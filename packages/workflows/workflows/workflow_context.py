from dataclasses import dataclass

from shared.services.context_collector import ContextCollector

from agents.triage.triage_service import TriageService


@dataclass(slots=True)
class WorkflowContext:
    context_collector: ContextCollector
    triage_service: TriageService