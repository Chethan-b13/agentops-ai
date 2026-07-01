import time
from pathlib import Path
from dotenv import load_dotenv

# Load env variables from root .env
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from sqlalchemy.orm import Session
from shared.database.session import SessionLocal
from shared.services import IncidentProcessingService
from shared.settings import settings
from shared.evaluation import (
    EvaluationConfig,
    WorkflowResult,
    Benchmark,
)
from shared.observability import (
    initialize_langfuse,
    set_current_trace,
)
from workflows.factory import create_workflow
from eval_engine.adapter import BenchmarkAdapter
from eval_engine.evaluator import Evaluator
from eval_engine.console import Console

def run_dataset_eval(experiment_name: str):
    print("Initializing Langfuse client...")
    langfuse = initialize_langfuse()
    
    dataset_name = "agentops-incident-benchmarks"
    print(f"Fetching Langfuse dataset '{dataset_name}'...")
    try:
        dataset = langfuse.get_dataset(dataset_name)
    except Exception as e:
        print(f"❌ Failed to fetch dataset. Make sure you run upload_to_langfuse.py first! Error: {e}")
        return

    evaluator = Evaluator()
    adapter = BenchmarkAdapter()

    # Resolve model name from the active provider
    _active_model = (
        settings.gemini_model
        if settings.llm_provider == "gemini"
        else settings.ollama_model
    )
    config = EvaluationConfig(
        model=_active_model,
        provider=settings.llm_provider,
        prompt_version="v1",
    )
    print(f"🤖 LLM Provider : {settings.llm_provider.upper()} ({_active_model})")
    
    total = len(dataset.items)
    passed = 0
    
    print(f"\n🚀 Running experiments on '{dataset_name}' (Experiment Run: '{experiment_name}')")
    print(f"Total benchmarks: {total}\n" + "-"*40)
    
    for idx, item in enumerate(dataset.items, 1):
        # Merge input & expected output to reconstruct Benchmark model
        bm_dict = {**item.input, "expected_outputs": item.expected_output}
        benchmark = Benchmark.model_validate(bm_dict)
        
        print(f"[{idx}/{total}] Running Benchmark: {benchmark.id} - {benchmark.name}")
        
        # 1. Create a Langfuse trace for this run
        trace = langfuse.trace(
            name="Incident Workflow",
            user_id="eval-engine",
            metadata={
                "benchmark_id": benchmark.id,
                "difficulty": benchmark.difficulty,
                "experiment_name": experiment_name,
            }
        )
        
        # 2. Link this trace to the dataset item and the experiment name
        item.link(trace, run_name=experiment_name)
        
        # 3. Set trace context so LLMClient automatically logs generations inside this trace
        set_current_trace(trace)
        
        db: Session = SessionLocal()
        try:
            processing_service = IncidentProcessingService(db)
            incident = adapter.create_incident(benchmark)
            incident = processing_service.process(incident)
            
            start = time.perf_counter()
            
            with create_workflow(db) as graph:
                state = graph.invoke(
                    {"incident_id": incident.id},
                    config={"configurable": {"thread_id": incident.id}},
                )
                
            latency_ms = (time.perf_counter() - start) * 1000
            
            result = WorkflowResult(
                incident_id=incident.id,
                triage=state["triage_result"].model_dump(),
                rca=state["rca_result"].model_dump(),
                remediation=state["remediation_plan"].model_dump(),
                validation=state["validation_result"].model_dump(),
                latency_ms=latency_ms,
            )
            
            evaluation = evaluator.evaluate(benchmark, result)
            
            print(f"   ✓ Executed workflow. Score: {evaluation['score']:.2f} | Passed: {evaluation['passed']}")
            print(f"   Reasoning: {evaluation['reasoning']}")
            
            if evaluation["passed"]:
                passed += 1
                
            # 4. Upload evaluation scores back to Langfuse
            langfuse.score(
                trace_id=trace.id,
                name="rca_score",
                value=evaluation["score"],
                comment=evaluation["reasoning"]
            )
            langfuse.score(
                trace_id=trace.id,
                name="passed",
                value=1 if evaluation["passed"] else 0,
            )
            langfuse.score(
                trace_id=trace.id,
                name="latency",
                value=latency_ms,
            )
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            langfuse.score(
                trace_id=trace.id,
                name="passed",
                value=0,
                comment=f"Error during execution: {str(e)}"
            )
        finally:
            db.close()
            # Clear trace context
            set_current_trace(None)
            
    # Flush all remaining events to Langfuse
    langfuse.flush()
    print("-"*40)
    print(f"Experiment Run '{experiment_name}' completed. Passed {passed}/{total} benchmarks.")
    print("View the results, comparisons, and full traces in your Langfuse UI (http://localhost:3000)")

if __name__ == "__main__":
    import sys
    # Use command-line arg for experiment name, default to timestamp
    exp_name = sys.argv[1] if len(sys.argv) > 1 else f"run_{int(time.time())}"
    run_dataset_eval(exp_name)
