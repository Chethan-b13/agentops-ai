from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)


def build_triage_messages(
    incident,
    evidence,
):

    return [

        SystemMessage(
            content="""
            You are an expert Site Reliability Engineer.

            Your task is to classify infrastructure incidents.

            You must determine:

            - severity
            - category
            - owning team
            - confidence

            Only use the provided evidence.
            """
        ),

        HumanMessage(
            content=f"""
            Incident:

            {incident}

            Evidence:

            {evidence}
            """
        ),
    ]