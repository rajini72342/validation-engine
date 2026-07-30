"""Data models for the Outcome Classifier service."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class VerdictType(str, Enum):
    """The four possible outcomes of a validation run."""

    DETECTED = "Detected"
    MISSED = "Missed"
    PARTIAL = "Partial"
    NO_DATA = "NoData"


class AlertFidelity(str, Enum):
    """How specifically an alert references the underlying technique."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class MatchedEvent(BaseModel):
    """A single defensive/SIEM event that matched (fully or partially)
    against the expected observable for an evidence event."""

    event_id: str
    rule_id: Optional[str] = None
    alert_name: Optional[str] = None
    matched_fields: List[str] = Field(default_factory=list)
    technique_ref_in_alert: Optional[str] = None
    timestamp: Optional[datetime] = None
    raw: Dict = Field(default_factory=dict)


class RawValidationResult(BaseModel):
    """The raw output of the Validation Engine, before classification.

    This is the input contract the Outcome Classifier consumes.
    """

    action_id: str
    technique_ref: str
    rule_id: str
    confidence: float = Field(ge=0.0, le=1.0)
    expected_observable: str
    expected_fields: List[str] = Field(default_factory=list)
    matched_events: List[MatchedEvent] = Field(default_factory=list)
    no_data: bool = False
    evidence_timestamp: Optional[datetime] = None
    tenant_id: Optional[str] = None


class CausalStep(BaseModel):
    """A single step in the causal chain explaining a verdict."""

    step_number: int
    description: str
    evidence_ref: Optional[str] = None


class OutcomeVerdict(BaseModel):
    """The final classified outcome for a single evidence event."""

    action_id: str
    technique_ref: str
    rule_id: str
    verdict: VerdictType
    confidence: float = Field(ge=0.0, le=1.0)
    causal_chain: List[CausalStep] = Field(default_factory=list)
    mttd_seconds: Optional[float] = None
    alert_fidelity: Optional[AlertFidelity] = None
    matched_evidence_ref: Optional[str] = None
