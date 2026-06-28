from dataclasses import dataclass

from shared.services.context_collector import ContextCollector

from agents.triage.triage_service import TriageService
from agents.rca.rca_service import RCAService
from agents.remediation.remediation_service import RemediationService

from shared.services.knowledge_retriever import (
    KnowledgeRetriever,
)


@dataclass(slots=True)
class WorkflowContext:
    context_collector: ContextCollector
    triage_service: TriageService
    knowledge_retriever: KnowledgeRetriever
    rca_service: RCAService
    remediation_service: RemediationService