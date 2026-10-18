"""
Tests for clinical information and medication extraction.
"""

import pytest
from app.core.clinical_nlp import (
    extract_clinical_information,
    extract_patient_info,
    extract_medications,
    extract_warning_signs,
    extract_follow_up
)
from app.data.synthetic_samples import SYNTHETIC_SAMPLES


def test_diabetes_sample_extraction():
    sample = SYNTHETIC_SAMPLES[0]["raw_text"]
    extraction = extract_clinical_information(sample)

    assert extraction.patient_name == "Ramesh Kumar"
    assert "Diabetes" in str(extraction.conditions)
    
    # Check medications
    med_names = [m.name.lower() for m in extraction.medications]
    assert any("metformin" in n for n in med_names)
    assert any("glimepiride" in n for n in med_names)
    assert any("telmisartan" in n for n in med_names)
    assert any("methylcobalamin" in n for n in med_names)

    # Check dose & unit
    metformin = next(m for m in extraction.medications if "metformin" in m.name.lower())
    assert "500 mg" in metformin.dose_and_unit
    assert metformin.strength_value == 500.0
    assert "Twice daily" in metformin.frequency

    # Check warning signs
    assert len(extraction.warning_signs) > 0
    warning_text = " ".join([w.sign for w in extraction.warning_signs]).lower()
    assert "hypoglycemia" in warning_text or "sweating" in warning_text

    # Check follow up
    assert len(extraction.follow_ups) > 0
    assert "28-Oct-2026" in extraction.follow_ups[0].date


def test_surgery_sample_extraction():
    sample = SYNTHETIC_SAMPLES[1]["raw_text"]
    extraction = extract_clinical_information(sample)

    assert extraction.patient_name == "Sunita Devi"
    assert extraction.patient_gender == "Female"
    
    med_names = [m.name.lower() for m in extraction.medications]
    assert any("cefuroxime" in n for n in med_names)
    assert any("pantoprazole" in n for n in med_names)
    assert any("paracetamol" in n for n in med_names)
    assert any("tramadol" in n for n in med_names)

    # Tramadol should have SOS/PRN
    tramadol = next(m for m in extraction.medications if "tramadol" in m.name.lower())
    assert "SOS" in tramadol.frequency or "needed" in tramadol.frequency.lower()

    # Wound care
    assert len(extraction.wound_care_instructions) > 0
