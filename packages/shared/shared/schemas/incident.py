from enum import Enum

class IncidentStatus(str, Enum):
    NEW = "new"
    COLLECTING_EVIDENCE = "collecting_evidence"
    EVIDENCE_COLLECTED = "evidence_collected"
    TRIAGING = "triaging"
    TRIAGED = "triaged"
    INVESTIGATING = "investigating"
    FIX_RECOMMENDED = "fix_recommended"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    RESOLVED = "resolved"
    FAILED = "failed"