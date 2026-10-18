"""
Tests for FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.data.synthetic_samples import SYNTHETIC_SAMPLES

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["service"] == "CareBridge AI"


def test_get_demo_samples():
    response = client.get("/api/demo-samples")
    assert response.status_code == 200
    samples = response.json()
    assert len(samples) >= 5
    assert samples[0]["patient_name"] != ""


def test_generate_care_plan_endpoint():
    sample = SYNTHETIC_SAMPLES[0]["raw_text"]
    response = client.post("/api/generate", json={
        "text": sample,
        "languages": ["en", "te"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "english_plan" in data
    assert "telugu_plan" in data
    assert "faithfulness_report" in data
    assert data["faithfulness_report"]["overall_status"] == "VERIFIED"
    assert "readability" in data


def test_validate_endpoint():
    sample = SYNTHETIC_SAMPLES[0]["raw_text"]
    # First generate
    gen_resp = client.post("/api/generate", json={"text": sample})
    gen_data = gen_resp.json()

    # Validate
    val_resp = client.post("/api/validate", json={
        "source_text": sample,
        "english_plan": gen_data["english_plan"],
        "telugu_plan": gen_data["telugu_plan"]
    })
    assert val_resp.status_code == 200
    val_data = val_resp.json()
    assert val_data["overall_status"] == "VERIFIED"


def test_fridge_sheet_download():
    sample = SYNTHETIC_SAMPLES[0]["raw_text"]
    gen_resp = client.post("/api/generate", json={"text": sample})
    plan_id = gen_resp.json()["id"]

    # Test PDF download
    pdf_resp = client.get(f"/api/fridge-sheet?plan_id={plan_id}&format=pdf&lang=en")
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"] == "application/pdf"

    # Test HTML printable view
    html_resp = client.get(f"/api/fridge-sheet?plan_id={plan_id}&format=html&lang=en")
    assert html_resp.status_code == 200
    assert "html" in html_resp.headers["content-type"]


def test_assistant_chat_multilingual():
    sample = SYNTHETIC_SAMPLES[0]["raw_text"]
    gen_resp = client.post("/api/generate", json={"text": sample})
    plan_id = gen_resp.json()["id"]

    # 1. English
    en_resp = client.post("/api/assistant/chat", json={
        "message": "When should I take Metformin?",
        "language": "en",
        "plan_id": plan_id
    })
    assert en_resp.status_code == 200
    en_data = en_resp.json()
    assert len(en_data["reply"]) > 10
    assert en_data["voice_lang_code"] == "en-US"

    # 2. Telugu
    te_resp = client.post("/api/assistant/chat", json={
        "message": "నా మందులు ఎప్పుడు వేసుకోవాలి?",
        "language": "te",
        "plan_id": plan_id
    })
    assert te_resp.status_code == 200
    te_data = te_resp.json()
    assert len(te_data["reply"]) > 10
    assert te_data["voice_lang_code"] == "te-IN"

    # 3. Hindi
    hi_resp = client.post("/api/assistant/chat", json={
        "message": "दवाएं कब लेनी हैं?",
        "language": "hi",
        "plan_id": plan_id
    })
    assert hi_resp.status_code == 200
    hi_data = hi_resp.json()
    assert len(hi_data["reply"]) > 10
    assert hi_data["voice_lang_code"] == "hi-IN"

    # 4. Tamil
    ta_resp = client.post("/api/assistant/chat", json={
        "message": "மருந்துகள் எப்போது சாப்பிட வேண்டும்?",
        "language": "ta",
        "plan_id": plan_id
    })
    assert ta_resp.status_code == 200
    ta_data = ta_resp.json()
    assert len(ta_data["reply"]) > 10
    assert ta_data["voice_lang_code"] == "ta-IN"

