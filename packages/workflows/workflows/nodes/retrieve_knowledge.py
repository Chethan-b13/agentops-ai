from shared.services.knowledge_retriever import (
    KnowledgeRetriever,
)

from workflows.state import (
    IncidentWorkflowState,
)


def create_retrieve_knowledge_node(
    retriever: KnowledgeRetriever,
):

    def retrieve_knowledge_node(
        state: IncidentWorkflowState,
    ) -> IncidentWorkflowState:

        documents = retriever.retrieve(
            state["incident_id"]
        )

        return {
            **state,
            "knowledge_documents": documents,
        }

    return retrieve_knowledge_node