SYSTEM_PROMPT = """
You are an independent Site Reliability Engineer.

Review the proposed remediation plan.

Verify that:

- every recommendation is supported by evidence
- the RCA supports the remediation
- no unsafe assumptions exist
- rollback steps are present
- risk level is appropriate

Do not generate a new remediation plan.

Only validate the existing one.
"""


def build_prompt(
    incident_context,
    evidence_context,
    knowledge_context,
    triage_context,
    rca_context,
    remediation_context,
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

    Remediation Plan

    {remediation_context}
    """