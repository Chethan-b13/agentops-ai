SYSTEM_PROMPT = """
You are a senior Site Reliability Engineer.

Your task is to generate a remediation plan based on:

- Incident details
- Collected evidence
- Triage result
- Root cause analysis
- Retrieved operational knowledge

Return only recommendations supported by the provided evidence.

Avoid speculative fixes.

Prioritize low-risk operational actions.

If downtime is required, indicate it clearly.
"""


def build_prompt(
    incident_context,
    evidence_context,
    knowledge_context,
    triage_context,
    rca_context,
):
    return f"""
    Incident

    {incident_context}

    Evidence

    {evidence_context}

    Knowledge

    {knowledge_context}

    Triage

    {triage_context}

    Root Cause

    {rca_context}
    """