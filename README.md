# Outcome Classifier (Pod Beta)

CyBreach Module 2: The Validator - Outcome Classifier microservice.

Converts raw validation results (rule execution vs. evidence) into
classified verdicts, per section 3.4 of the Module 2 Technical Doc.

## What it does

- **Verdict classification** - turns a `RawValidationResult` into one of
  four verdicts: `Detected`, `Missed`, `Partial`, `NoData`.
- **Causal chain analysis** - builds a deterministic, step-by-step
  reasoning trail explaining why a verdict was assigned.
- **Alert fidelity assessment** - classifies `Detected`/`Partial` alerts
  as `high`, `medium`, or `low` fidelity based on technique specificity
  and expected-field coverage.
- **MTTD computation** - measures Mean Time To Detect (seconds) between
  the simulated attack (evidence timestamp) and the first matching
  alert.

## Classification thresholds

| Verdict  | Confidence range | Notes                                   |
|----------|-------------------|------------------------------------------|
| Detected | 0.7 - 1.0         | Rule fired, evidence matched expectation |
| Partial  | 0.3 - 0.6         | Some but not all observables matched     |
| Missed   | 0.0 - 0.2         | No matching evidence found                |
| NoData   | N/A               | `no_data=True` always takes precedence   |

## Project layout

```
outcome_classifier/
  __init__.py
  models.py          # Pydantic models (RawValidationResult, OutcomeVerdict, ...)
  classifier.py       # OutcomeClassifier - verdict thresholds & orchestration
  causal_chain.py      # CausalChainBuilder - step-by-step reasoning
  fidelity.py          # FidelityAssessor - high/medium/low fidelity scoring
  mttd.py              # compute_mttd_seconds - MTTD calculation
  app.py                # FastAPI wrapper (POST /classify, GET /health)
tests/
  conftest.py           # shared fixtures
  test_classifier.py
  test_causal_chain.py
  test_fidelity.py
  test_mttd.py
  test_app.py
```

## Local setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the full test suite with coverage
pytest --cov=outcome_classifier --cov-report=term-missing

# Run the service locally
uvicorn outcome_classifier.app:app --reload --port 8003
curl http://localhost:8003/health
```

## Example usage (library)

```python
from datetime import datetime, timezone
from outcome_classifier import OutcomeClassifier, RawValidationResult, MatchedEvent

result = RawValidationResult(
    action_id="action-001",
    technique_ref="T1486",
    rule_id="rule-ransomware-001",
    confidence=0.95,
    expected_observable="mass file encryption via vssadmin/wbadmin",
    expected_fields=["CommandLine", "Image", "host"],
    matched_events=[
        MatchedEvent(
            event_id="evt-001",
            matched_fields=["CommandLine", "Image", "host"],
            technique_ref_in_alert="T1486",
            timestamp=datetime(2026, 6, 1, 12, 0, 42, tzinfo=timezone.utc),
        )
    ],
    evidence_timestamp=datetime(2026, 6, 1, 12, 0, 0, tzinfo=timezone.utc),
)

verdict = OutcomeClassifier().classify(result)
print(verdict.verdict)          # VerdictType.DETECTED
print(verdict.alert_fidelity)   # AlertFidelity.HIGH
print(verdict.mttd_seconds)     # 42.0
```

## Contract notes

- Input (`RawValidationResult`) is what Pod Beta's Validation Engine
  produces internally; it is not the published Module 2 contract.
- Output (`OutcomeVerdict`) maps onto the published Verdict Schema
  fields (`verdict`, `confidence`, `mttd`, `causal_chain`,
  `matched_evidence_ref`) that the Verdict Publisher consumes before
  emitting immutable events to `cybreach.verdicts.v2`.
