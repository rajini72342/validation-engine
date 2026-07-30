from fastapi.testclient import TestClient

from outcome_classifier.app import app

client = TestClient(app)


def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_classify_endpoint_returns_detected_verdict():
    payload = {
        "action_id": "action-http-001",
        "technique_ref": "T1486",
        "rule_id": "rule-ransomware-001",
        "confidence": 0.95,
        "expected_observable": "mass file encryption",
        "expected_fields": ["CommandLine", "Image", "host"],
        "matched_events": [
            {
                "event_id": "evt-http-001",
                "matched_fields": ["CommandLine", "Image", "host"],
                "technique_ref_in_alert": "T1486",
                "timestamp": "2026-06-01T12:00:42Z",
            }
        ],
        "no_data": False,
        "evidence_timestamp": "2026-06-01T12:00:00Z",
        "tenant_id": "tenant-alpha",
    }
    resp = client.post("/classify", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["verdict"] == "Detected"
    assert body["alert_fidelity"] == "high"
    assert body["mttd_seconds"] == 42.0
