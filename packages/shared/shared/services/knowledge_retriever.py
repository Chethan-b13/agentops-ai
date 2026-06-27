from shared.schemas.knowledge import KnowledgeDocument

class KnowledgeRetriever:

    def retrieve( self, incident_id: str) -> list[KnowledgeDocument]:
        return [
            KnowledgeDocument(
                source="runbook",
                title="Database Timeout",
                content=(
                    "Investigate database connection pool "
                    "and recent deployments."
                ),
                score=0.97,
            ),
            KnowledgeDocument(
                source="postmortem",
                title="Payments API Outage",
                content=(
                    "Similar incident caused by exhausted "
                    "PostgreSQL connections."
                ),
                score=0.91,
            ),
        ]