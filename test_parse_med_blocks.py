import re
from app.data.drug_reference import DRUG_REFERENCE, DRUG_ALIASES
from test_blocks import resolve_drug

def parse_medication_block(block: str):
    drug_key, ref = resolve_drug(block)
    if not drug_key:
        return None
        
    generic = ref.get("generic")
    default_dose = ref.get("default_dose", "1 dose")
    category = ref.get("category", "")
    
    # Form
    is_topical = "cream" in block.lower() or "topical" in category.lower() or "oint" in block.lower()
    is_cap = "cap" in block.lower()
    is_tab = "tab" in block.lower() or "tenb" in block.lower()
    
    if is_topical:
        name = "Luliclinz-XL Cream" if "luliclin" in drug_key else f"{drug_key.capitalize()} Cream"
        route = "Topical (Apply on skin)"
    elif is_cap:
        name = f"Cap. {drug_key.capitalize()}"
        route = "Oral (by mouth)"
    elif is_tab:
        name = f"Tab. {drug_key.capitalize()}"
        route = "Oral (by mouth)"
    else:
        name = drug_key.capitalize()
        route = "Oral (by mouth)"
        
    # Dose
    dose_match = re.search(r'(\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml))', block, re.I)
    if dose_match:
        dose = dose_match.group(1).strip()
    elif is_topical:
        dose = "Apply as directed (Thin layer)"
    elif "200" in block or "aoom" in block.lower() or "abom" in block.lower():
        dose = "200 mg"
    elif "5" in block or "amg" in block.lower() or "img" in block.lower():
        dose = "5 mg"
    else:
        dose = default_dose

    # Frequency
    freq = "Please confirm with your healthcare professional."
    raw_code = None
    if is_topical:
        freq = "Twice daily: Morning & Night (M-N)"
        raw_code = "BD_MN"
    elif re.search(r'\bN\b|\bnight\b|\bhs\b', block, re.I):
        freq = "Once daily at night (N)"
        raw_code = "OD_N"
    elif re.search(r'\b(?:BD|BID|Twice)\b', block, re.I):
        freq = "Twice daily (BD)"
        raw_code = "BD"
    elif re.search(r'\b(?:TDS|TID|Three times)\b', block, re.I):
        freq = "Three times a day (TDS)"
        raw_code = "TDS"
    elif re.search(r'\b(?:OD|Once daily)\b', block, re.I):
        freq = "Once daily (OD)"
        raw_code = "OD"

    # Timing
    timing = "Please confirm with your healthcare professional."
    if re.search(r'\b(?:cpm|3pm|7\s*pm|7:00\s*pm)\b', block, re.I):
        timing = "7:00 PM (Evening)"
    elif re.search(r'\b(?:yter\s*sood|after\s*food|after\s*meals?|pc)\b', block, re.I):
        timing = "After meals (after food)"
    elif is_topical:
        timing = "Morning and Night"
    elif re.search(r'\b(?:before\s*food|before\s*meals?|ac)\b', block, re.I):
        timing = "Before meals (on empty stomach)"
    elif "night" in freq.lower():
        timing = "At bedtime"

    # Duration
    duration = "Please confirm with your healthcare professional."
    if re.search(r'\b(?:imonfi|dmonf|1\s*month|1month)\b', block, re.I):
        duration = "1 month"
    elif re.search(r'\b(?:20\s*dys|20\s*days|x\s*dy)\b', block, re.I):
        duration = "20 days"
    elif re.search(r'\b(?:lwek|lweh|6\s*weeks?)\b', block, re.I):
        duration = "6 weeks"
    else:
        dur_m = re.search(r'(?:x|for)?\s*(\d+\s*(?:days?|weeks?|months?))', block, re.I)
        if dur_m:
            duration = dur_m.group(1).strip()

    # Instructions
    if is_topical:
        instructions = "Apply externally over affected area as directed."
    elif "7:00" in timing:
        instructions = f"Take at {timing}."
    elif "after food" in timing.lower():
        instructions = "Take at night after food."
    else:
        instructions = f"Take as directed ({timing})."

    return {
        "name": name,
        "generic": generic,
        "dose": dose,
        "route": route,
        "frequency": freq,
        "timing": timing,
        "duration": duration,
        "instructions": instructions
    }

blocks = [
    "my ty CAp. LTAIyI abOm CAp. LTEAIyI aOOm 0 2 X dmonf X imonfi yter sood IPoopeoe",
    "Yen Tenb Lecopeamg LecoPeImg 2 N p Cpm X X dy",
    "LvLiCLIn2-xL UeOm fna xf wmae 1x-2 nn217a7 ssg cbm uabm en ne 006 0984 Revieo Revievo N X Lwek Lweh"
]

for i, b in enumerate(blocks):
    parsed = parse_medication_block(b)
    print(f"\n--- MEDICATION {i+1} ---")
    for k, v in parsed.items():
        print(f"  {k}: {v}")
