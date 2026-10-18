import sys
from app.core.pdf_extractor import extract_text_from_file
from app.core.clinical_nlp import extract_clinical_information
from app.core.translator import build_telugu_care_plan
from app.core.faithfulness import run_faithfulness_audit
from app.core.timetable import generate_seven_day_timetable

pdf_path = r"C:\Users\bhavy\Downloads\prescription doctor.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# 1. OCR Extraction
text, meta = extract_text_from_file(pdf_bytes, "prescription doctor.pdf")
print("=== EXTRACTED TEXT FROM PDF ===")
print(text)
print("\n=== METADATA ===")
print(meta)

# 2. Clinical Extraction
ext = extract_clinical_information(text)
print("\n=== CLINICAL EXTRACTION ===")
print("Patient Name:", ext.patient_name)
print("Conditions:", ext.conditions)
print(f"Total Medications: {len(ext.medications)}")
for i, m in enumerate(ext.medications):
    print(f"\n[Medication {i+1}]")
    print(f"  Name: {m.name}")
    print(f"  Generic: {m.generic_name}")
    print(f"  Dose: {m.dose_and_unit}")
    print(f"  Frequency: {m.frequency}")
    print(f"  Timing: {m.timing}")
    print(f"  Duration: {m.duration}")
    print(f"  Route: {m.route}")
    print(f"  Instructions: {m.instructions}")

print(f"\nFollow-ups: {len(ext.follow_ups)}")
for f in ext.follow_ups:
    print(f"  • Date: {f.date} | Clinician: {f.clinician_or_department} | Instr: {f.instructions}")

# 3. Telugu Translation
telugu_plan = build_telugu_care_plan(ext)
print("\n=== TELUGU CARE PLAN MEDICINES ===")
for m in telugu_plan["medicines"]:
    print(f"  • {m['name']} ({m.get('generic', '')}) - {m['dose_and_unit']} | {m['frequency']} | {m['timing']}")

# 4. Timetable
timetable = generate_seven_day_timetable(ext.medications)
print("\n=== 7-DAY TIMETABLE SCHEDULE ===")
day1 = timetable.get("Day 1", {})
for slot, meds in day1.items():
    if meds:
        print(f"  {slot}: {[m['name'] + ' ' + m['dose'] for m in meds]}")

# 5. Faithfulness Report
english_plan = {
    "medicines": [m.model_dump() for m in ext.medications],
    "warning_signs": [w.model_dump() for w in ext.warning_signs],
    "diet_instructions": ext.diet_instructions,
    "activity_restrictions": ext.activity_restrictions,
    "wound_care_instructions": ext.wound_care_instructions,
    "follow_ups": [f.model_dump() for f in ext.follow_ups]
}
audit = run_faithfulness_audit(text, ext, english_plan, telugu_plan)
print("\n=== FAITHFULNESS AUDIT ===")
print("Overall Status:", audit.overall_status)
print("Fact Preservation Rate:", audit.metrics["fact_preservation_rate"])
print("Hard Safety Gate Triggered:", audit.hard_safety_gate_triggered)
print("Checks:")
for c in audit.checks:
    print(f"  [{c.status}] {c.category}: {c.details}")
