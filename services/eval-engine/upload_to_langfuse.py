import os
from pathlib import Path
from dotenv import load_dotenv

# Load env variables from root .env
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from shared.observability.langfuse import initialize_langfuse
from eval_engine.discovery import BenchmarkDiscovery
from eval_engine.loader import BenchmarkLoader

def main():
    print("Initializing Langfuse client...")
    langfuse = initialize_langfuse()
    
    dataset_name = "agentops-incident-benchmarks"
    print(f"Checking/Creating Langfuse dataset '{dataset_name}'...")
    try:
        dataset = langfuse.get_dataset(dataset_name)
        print(f"Dataset '{dataset_name}' already exists.")
    except Exception:
        dataset = langfuse.create_dataset(
            name=dataset_name,
            description=(
                "Production-style synthetic incident benchmarks used to "
                "evaluate the AgentOps AI autonomous incident response workflow. "
                "Each dataset item contains incident context, evidence, and "
                "expected triage, RCA, remediation, and validation outputs."
            ),
        )
        print(f"Created new dataset '{dataset_name}'.")

    # Get existing items to avoid duplicates
    existing_benchmark_ids = {
        item.input.get("id")
        for item in dataset.items
        if isinstance(item.input, dict)
        and item.input.get("id")
    }

    discovery = BenchmarkDiscovery()
    loader = BenchmarkLoader()
    
    benchmark_dir = Path(__file__).resolve().parents[2] / "datasets" / "benchmarks"
    benchmarks = discovery.discover(benchmark_dir)
    
    print(f"Found {len(benchmarks)} local benchmark files.")
    uploaded_count = 0
    
    for bm_path in benchmarks:
        try:
            benchmark = loader.load(bm_path)
            # Check if already uploaded
            if benchmark.id in existing_benchmark_ids:
                print(f"⏭ Skipping {benchmark.id} (already uploaded)")
                continue
                
            print(f"Uploading benchmark {benchmark.id} ({benchmark.name})...")
            
            # Serialize the benchmark object to dict
            bm_data = benchmark.model_dump()
            
            # Separate input (context details) and expected output
            # Input contains everything needed to trigger/run the workflow
            item_input = {
                "id": bm_data["id"],
                "name": bm_data["name"],
                "description": bm_data["description"],
                "tags": bm_data["tags"],
                "difficulty": bm_data["difficulty"],
                "source": bm_data["source"],
                "version": bm_data["version"],
                "metadata": bm_data["metadata"],
                "incident": bm_data["incident"],
                "evidence": bm_data["evidence"]
            }
            
            item_expected = bm_data["expected_outputs"]
            
            langfuse.create_dataset_item(
                dataset_name=dataset_name,
                input=item_input,
                expected_output=item_expected,
                metadata={
                    "benchmark_id": benchmark.id,
                    "benchmark_name": benchmark.name,
                    "category": benchmark.expected_outputs.triage.category,
                    "service": benchmark.incident.service,
                    "severity": benchmark.incident.severity,
                    "difficulty": benchmark.difficulty,
                    "tags": benchmark.tags,
                    "version": benchmark.version,
                },
            )
            uploaded_count += 1
            print(f"✓ Uploaded {benchmark.id}")
            
        except Exception as e:
            print(f"❌ Failed to upload benchmark from {bm_path}: {e}")

    langfuse.flush() 
    print(f"\nUpload complete! Uploaded {uploaded_count} new benchmarks to Langfuse.")

if __name__ == "__main__":
    main()
