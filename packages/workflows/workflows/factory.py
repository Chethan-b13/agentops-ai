from contextlib import contextmanager

from shared.repositories.incident_repository import IncidentRepository
from shared.repositories.incident_evidence_repository import IncidentEvidenceRepository
from shared.repositories.triage_repository import TriageRepository
from shared.repositories.rca_repository import RCARepository
from shared.repositories.remediation_repository import RemediationRepository
from shared.repositories.validation_repository import ValidationRepository

from shared.services.context_collector import ContextCollector
from shared.services.knowledge_retriever import KnowledgeRetriever
from shared.services.execution_service import ExecutionService

from shared.clients.github_client import GitHubClient
from shared.executors.github_executor import GitHubExecutor

from agents.triage.triage_agent import TriageAgent
from agents.triage.triage_service import TriageService

from agents.rca.rca_agent import RCAAgent
from agents.rca.rca_service import RCAService

from agents.remediation.remediation_agent import RemediationAgent
from agents.remediation.remediation_service import RemediationService

from agents.validation.validation_agent import ValidationAgent
from agents.validation.validation_service import ValidationService

from shared.settings import settings

from workflows.workflow_context import WorkflowContext
from workflows.graphs.investigation_graph import create_investigation_graph
from workflows.checkpointer import create_checkpointer


@contextmanager
def create_workflow(db):

    incident_repo = IncidentRepository(db)
    evidence_repo = IncidentEvidenceRepository(db)

    context_collector = ContextCollector(
        incident_repo,
        evidence_repo,
    )

    triage_service = TriageService(
        incident_repo=incident_repo,
        evidence_repo=evidence_repo,
        triage_repo=TriageRepository(db),
        triage_agent=TriageAgent(),
    )

    knowledge_retriever = KnowledgeRetriever()

    rca_service = RCAService(
        incident_repo=incident_repo,
        evidence_repo=evidence_repo,
        rca_repo=RCARepository(db),
        rca_agent=RCAAgent(),
    )

    remediation_service = RemediationService(
        incident_repo=incident_repo,
        evidence_repo=evidence_repo,
        remediation_repo=RemediationRepository(db),
        remediation_agent=RemediationAgent(),
    )

    validation_service = ValidationService(
        incident_repo=incident_repo,
        evidence_repo=evidence_repo,
        validation_repo=ValidationRepository(db),
        validation_agent=ValidationAgent(),
    )

    github_client = GitHubClient(
        token=settings.github_token,
        repository=settings.github_repository,
    )

    execution_service = ExecutionService(
        GitHubExecutor(github_client)
    )

    workflow_context = WorkflowContext(
        context_collector=context_collector,
        triage_service=triage_service,
        knowledge_retriever=knowledge_retriever,
        rca_service=rca_service,
        remediation_service=remediation_service,
        validation_service=validation_service,
        execution_service=execution_service,
    )

    with create_checkpointer() as checkpointer:

        graph = create_investigation_graph(
            workflow_context,
            checkpointer=checkpointer,
        )

        yield graph