"""FastAPI application for the Outcome Classifier service (Pod Beta).

Exposes a single endpoint that accepts a RawValidationResult and
returns the classified OutcomeVerdict.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from .classifier import OutcomeClassifier
from .models import OutcomeVerdict, RawValidationResult

app = FastAPI(
    title="Outcome Classifier",
    description="CyBreach Module 2: The Validator - Outcome Classifier Service",
    version="1.0.0",
)

classifier = OutcomeClassifier()


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "outcome_classifier"}


@app.post("/classify", response_model=OutcomeVerdict)
async def classify(result: RawValidationResult) -> OutcomeVerdict:
    try:
        return classifier.classify(result)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc
