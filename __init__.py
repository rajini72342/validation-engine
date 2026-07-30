"""
Outcome Classifier Service (Pod Beta)
CyBreach Module 2: The Validator

Converts raw validation results (rule execution vs. evidence) into
classified verdicts (Detected / Missed / Partial / NoData), with
causal chain reasoning, alert fidelity assessment, and MTTD computation.
"""

from .models import (
    VerdictType,
    AlertFidelity,
    CausalStep,
    RawValidationResult,
    MatchedEvent,
    OutcomeVerdict,
)
from .classifier import OutcomeClassifier
from .causal_chain import CausalChainBuilder
from .fidelity import FidelityAssessor
from .mttd import compute_mttd_seconds

__all__ = [
    "VerdictType",
    "AlertFidelity",
    "CausalStep",
    "RawValidationResult",
    "MatchedEvent",
    "OutcomeVerdict",
    "OutcomeClassifier",
    "CausalChainBuilder",
    "FidelityAssessor",
    "compute_mttd_seconds",
]
