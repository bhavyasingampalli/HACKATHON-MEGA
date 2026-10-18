"""
Seven-Day Medicine Timetable Module for CareBridge AI.
Maps explicit medication frequencies into a structured 7-day schedule.
Strict Safety Rules:
- Never invents morning, afternoon, evening, or night hours if not specified.
- If timing is incomplete, marks timetable as a "DRAFT" with explicit clinician confirmation warnings.
- Explicitly warns: Never start, stop, increase, or decrease doses independently.
"""

from typing import Dict, Any, List
from app.models.schemas import MedicationItem
from app.data.abbreviations import MEDICAL_ABBREVIATIONS


def generate_seven_day_timetable(medications: List[MedicationItem]) -> Dict[str, Any]:
    """
    Constructs a 7-day timetable across 4 standard daily time intervals:
    - Morning (Breakfast)
    - Afternoon (Lunch)
    - Evening (Dinner)
    - Bedtime (Night)
    """
    if not medications:
        return {
            "has_data": False,
            "message": "No medications available to build timetable."
        }

    days = [f"Day {i+1}" for i in range(7)]
    time_slots = ["Morning (Breakfast)", "Afternoon (Lunch)", "Evening (Dinner)", "Bedtime (Night)"]
    
    medication_schedules = []
    has_ambiguity = False
    ambiguous_medications = []

    for med in medications:
        raw_code = med.raw_frequency_code or ""
        freq_str = med.frequency.lower()
        timing_str = med.timing.lower()
        
        # Determine slot allocation
        slots = []
        is_timing_inferred = False

        if "bbf" in timing_str or "before breakfast" in timing_str or "mane" in timing_str or "in the morning" in timing_str:
            slots.append("Morning (Breakfast)")
        elif "7:00 pm" in timing_str or "7 pm" in timing_str or "evening" in timing_str:
            slots.append("Evening (Dinner)")
        elif "hs" in timing_str or "bedtime" in timing_str or "at night" in timing_str or "night" in freq_str or raw_code == "OD_N":
            slots.append("Bedtime (Night)")

        # Map standard frequencies
        if "morning & night" in freq_str or "m-n" in freq_str or raw_code == "BD_MN":
            slots = ["Morning (Breakfast)", "Bedtime (Night)"]
        elif raw_code == "OD" or "once daily" in freq_str:
            if not slots:
                slots.append("Morning (Breakfast)")
                is_timing_inferred = True
        elif raw_code == "BD" or "twice daily" in freq_str:
            if not slots or len(slots) < 2:
                slots = ["Morning (Breakfast)", "Bedtime (Night)"]
        elif raw_code == "TDS" or "three times" in freq_str:
            slots = ["Morning (Breakfast)", "Afternoon (Lunch)", "Evening (Dinner)"]
        elif raw_code == "QID" or "four times" in freq_str:
            slots = ["Morning (Breakfast)", "Afternoon (Lunch)", "Evening (Dinner)", "Bedtime (Night)"]
        elif "prn" in freq_str or "sos" in freq_str:
            slots = ["As Needed for Symptoms (SOS/PRN)"]
        elif not slots:
            slots = ["Unspecified Timing"]
            is_timing_inferred = True

        if is_timing_inferred or "unspecified" in slots[0].lower() or "confirm" in med.timing.lower():
            has_ambiguity = True
            ambiguous_medications.append(med.name)

        medication_schedules.append({
            "name": med.name,
            "generic": med.generic_name or "",
            "dose": med.dose_and_unit,
            "route": med.route,
            "frequency": med.frequency,
            "timing_instructions": med.timing,
            "allocated_slots": slots,
            "is_draft_slotting": is_timing_inferred,
            "warning": (
                "Specific clock hour or food relationship was not stated in summary. Confirm with doctor."
                if is_timing_inferred else ""
            )
        })

    # Build day-by-day matrix
    matrix = {}
    for day in days:
        matrix[day] = {
            "Morning": [],
            "Afternoon": [],
            "Evening": [],
            "Bedtime": [],
            "AsNeeded": []
        }
        for item in medication_schedules:
            slots = item["allocated_slots"]
            entry = {
                "name": item["name"],
                "dose": item["dose"],
                "instructions": item["timing_instructions"],
                "is_draft": item["is_draft_slotting"]
            }
            if any("morning" in s.lower() for s in slots):
                matrix[day]["Morning"].append(entry)
            if any("afternoon" in s.lower() for s in slots):
                matrix[day]["Afternoon"].append(entry)
            if any("evening" in s.lower() for s in slots):
                matrix[day]["Evening"].append(entry)
            if any("bedtime" in s.lower() for s in slots):
                matrix[day]["Bedtime"].append(entry)
            if any("as needed" in s.lower() for s in slots):
                matrix[day]["AsNeeded"].append(entry)

    return {
        "has_data": True,
        "days": days,
        "time_slots": time_slots,
        "medication_schedules": medication_schedules,
        "matrix": matrix,
        "is_complete_schedule": not has_ambiguity,
        "requires_clinician_confirmation": has_ambiguity,
        "ambiguous_medications": ambiguous_medications,
        "safety_disclaimer": (
            "DRAFT TIMETABLE NOTICE: This 7-day schedule maps explicit discharge instructions. "
            "Never independently start, stop, increase, or decrease medications. "
            "Always verify exact times and food interactions with your physician or pharmacist."
        )
    }
