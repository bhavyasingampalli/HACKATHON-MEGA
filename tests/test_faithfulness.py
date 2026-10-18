"""
Tests for Medical Faithfulness Checker & Hard Safety Gate.
"""

import pytest
from app.core.clinical_nlp import extract_clinical_information
from app.core.faithfulness import run_faithfulness_audit
from app.core.translator import build_telugu_care_plan
from app.data.synthetic_samples import SYNTHETIC_SAMPLES


@pytest.fixture
def clean_extraction_and_plan():
    raw_text = SYNTHETIC_SAMPLES[0]["raw_text"]
    ext = extract_clinical_information(raw_text)
    english_plan = {
        "medicines": [m.model_dump() for m in ext.medications],
        "warning_signs": [w.model_dump() for w in ext.warning_signs],
        "diet_instructions": ext.diet_instructions,
        "activity_restrictions": ext.activity_restrictions,
        "wound_care_instructions": ext.wound_care_instructions,
        "follow_ups": [f.model_dump() for f in ext.follow_ups]
    }
    telugu_plan = build_telugu_care_plan(ext)
    return raw_text, ext, english_plan, telugu_plan


def test_clean_plan_passes_all_checks(clean_extraction_and_plan):
    raw_text, ext, english_plan, telugu_plan = clean_extraction_and_plan
    report = run_faithfulness_audit(raw_text, ext, english_plan, telugu_plan)

    assert report.overall_status == "VERIFIED"
    assert not report.hard_safety_gate_triggered
    assert report.failed_checks == 0
    assert report.metrics["fact_preservation_rate"] == 100.0


def test_altered_dose_triggers_safety_gate(clean_extraction_and_plan):
    raw_text, ext, english_plan, telugu_plan = clean_extraction_and_plan
    
    # Tamper dose from 500 mg to 5000 mg
    english_plan["medicines"][0]["dose_and_unit"] = "5000 mg"

    report = run_faithfulness_audit(raw_text, ext, english_plan, telugu_plan)

    assert report.overall_status == "CLINICIAN_REVIEW_REQUIRED"
    assert report.hard_safety_gate_triggered is True
    assert any(c.category == "Dosage & Strength Verification" and c.status == "FAIL" for c in report.checks)


def test_altered_frequency_triggers_safety_gate(clean_extraction_and_plan):
    raw_text, ext, english_plan, telugu_plan = clean_extraction_and_plan
    
    # Tamper frequency from twice daily to once daily
    english_plan["medicines"][0]["frequency"] = "Once daily (OD)"

    report = run_faithfulness_audit(raw_text, ext, english_plan, telugu_plan)

    assert report.overall_status == "CLINICIAN_REVIEW_REQUIRED"
    assert report.hard_safety_gate_triggered is True
    assert any(c.category == "Intake Frequency" and c.status == "FAIL" for c in report.checks)


def test_omitted_emergency_warning_triggers_safety_gate(clean_extraction_and_plan):
    raw_text, ext, english_plan, telugu_plan = clean_extraction_and_plan
    
    # Omit hypoglycemia emergency signs
    english_plan["warning_signs"] = []

    report = run_faithfulness_audit(raw_text, ext, english_plan, telugu_plan)

    assert report.overall_status == "CLINICIAN_REVIEW_REQUIRED"
    assert report.hard_safety_gate_triggered is True
    assert any(c.category == "Emergency Warning Signs" and c.status == "FAIL" for c in report.checks)


def test_unsupported_medication_detected(clean_extraction_and_plan):
    raw_text, ext, english_plan, telugu_plan = clean_extraction_and_plan
    
    # Inject a hallucinated medication not in source
    english_plan["medicines"].append({
        "name": "Tab. Morphine 100 mg",
        "dose_and_unit": "100 mg",
        "frequency": "Once daily",
        "route": "Oral",
        "timing": "Morning",
        "duration": "10 days",
        "instructions": "Hallucinated"
    })

    report = run_faithfulness_audit(raw_text, ext, english_plan, telugu_plan)

    assert report.overall_status == "CLINICIAN_REVIEW_REQUIRED"
    assert report.hard_safety_gate_triggered is True
    assert any(c.category == "Unsupported Instructions (Hallucination)" and c.status == "FAIL" for c in report.checks)
