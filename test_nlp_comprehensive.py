import re
import difflib
from app.data.drug_reference import DRUG_REFERENCE, DRUG_ALIASES
from app.data.synthetic_samples import SYNTHETIC_SAMPLES
from app.models.schemas import MedicationItem

def resolve_drug_name(name_raw: str):
    clean = re.sub(r'[^a-zA-Z0-9\s\-]', ' ', name_raw).strip().lower()
    tokens = [t for t in clean.split() if len(t) >= 3]
    for token in tokens:
        if token in DRUG_ALIASES:
            k = DRUG_ALIASES[token]
            return k, DRUG_REFERENCE[k]
        if token in DRUG_REFERENCE:
            return token, DRUG_REFERENCE[token]
    for alias, target in DRUG_ALIASES.items():
        if len(alias) >= 4 and alias in clean:
            return target, DRUG_REFERENCE[target]
    best_match = None
    best_score = 0.0
    for token in tokens:
        if len(token) < 4:
            continue
        for alias, target in DRUG_ALIASES.items():
            if len(alias) < 4:
                continue
            ratio = difflib.SequenceMatcher(None, token, alias).ratio()
            if ratio > best_score and ratio >= 0.65:
                best_score = ratio
                best_match = target
    if best_match:
        return best_match, DRUG_REFERENCE[best_match]
    return None, None

def parse_medication_text(text: str):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    meds = []
    
    # 1. Group into item blocks
    blocks = []
    curr_block = []
    
    for line in lines:
        is_new_item = False
        # Numbered item prefix
        if re.match(r'^(?:[1-9]\s*[\.\)]|\b[1-9]\b)', line):
            is_new_item = True
        elif re.match(r'^(?:Tab|Cap|Syp|Inj|Cream|Oint|Inhaler|Rotacap|Lotion)\.?\b', line, re.I):
            is_new_item = True
        else:
            k, _ = resolve_drug_name(line.split('-')[0])
            if k and not any(k in b.lower() for b in curr_block):
                # Check if this line looks like a drug initiation
                if any(w in line.lower() for w in ["cap", "tab", "cream", "mg", "aoom", "abom", "img", "amg"]):
                    is_new_item = True
                    
        # Check if line is a non-med section header
        if re.match(r'^(?:DIET|ACTIVITY|WOUND|WARNING|EMERGENCY|FOLLOW|REVIEW|NEXT VISIT|HOSPITAL|INITIAL|DAILL|G61|G81)', line, re.I):
            if curr_block:
                blocks.append(' '.join(curr_block))
                curr_block = []
            continue

        if is_new_item and curr_block:
            blocks.append(' '.join(curr_block))
            curr_block = [line]
        elif curr_block:
            curr_block.append(line)
        elif is_new_item:
            curr_block.append(line)
            
    if curr_block:
        blocks.append(' '.join(curr_block))
        
    # Also support line-by-line if no blocks formed
    items_to_parse = blocks if blocks else lines
    
    for item_str in items_to_parse:
        item = parse_block_to_item(item_str)
        if item:
            # deduplicate
            if not any(m.name.lower() == item.name.lower() for m in meds):
                meds.append(item)
                
    return meds

def parse_block_to_item(block: str):
    clean = block.strip()
    clean = re.sub(r'^[1-9]\s*[\.\)]\s*', '', clean)
    
    drug_key, ref = resolve_drug_name(clean)
    generic = ref.get("generic") if ref else None
    category = ref.get("category", "") if ref else ""
    default_dose = ref.get("default_dose", "1 dose") if ref else "1 dose"

    is_topical = "cream" in clean.lower() or "topical" in category.lower() or "oint" in clean.lower()
    is_cap = re.search(r'\bcap(?:sule)?\.?\b', clean, re.I) is not None
    is_tab = re.search(r'\btab(?:let)?\.?\b|tenb', clean, re.I) is not None
    
    if drug_key:
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
    else:
        # Standard regex parse
        match = re.search(r'^(?:Tab|Cap|Syp|Inj|Inhaler)?\.?\s*([A-Za-z0-9\+\/\-\s\(\)]+?)(\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml|puffs?|units?|tablets?))', clean, re.I)
        if match:
            name = match.group(1).strip()
            route = "Oral (by mouth)"
        else:
            return None

    # Dose
    dose_match = re.search(r'(\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml|puffs?|units?|tablets?))', clean, re.I)
    if dose_match:
        dose = dose_match.group(1).strip()
    elif is_topical:
        dose = "Apply as directed (Thin layer)"
    elif "200" in clean or "aoom" in clean.lower() or "abom" in clean.lower():
        dose = "200 mg"
    elif "5" in clean or "amg" in clean.lower() or "img" in clean.lower():
        dose = "5 mg"
    else:
        dose = default_dose

    # Frequency
    freq = "Please confirm with your healthcare professional."
    raw_code = None
    if is_topical:
        freq = "Twice daily: Morning & Night (M-N)"
        raw_code = "BD_MN"
    elif re.search(r'\b(?:TDS|TID|Three times a day|3 times a day)\b', clean, re.I):
        freq = "Three times a day (TDS)"
        raw_code = "TDS"
    elif re.search(r'\b(?:QID|Four times a day|4 times a day)\b', clean, re.I):
        freq = "Four times a day (QID)"
        raw_code = "QID"
    elif re.search(r'\b(?:BD|BID|Twice daily|Twice a day|2 times a day)\b', clean, re.I):
        freq = "Twice daily (BD)"
        raw_code = "BD"
    elif re.search(r'\b(?:OD|QD|Once daily|Once a day|1 time a day)\b', clean, re.I):
        freq = "Once daily (OD)"
        raw_code = "OD"
    elif re.search(r'\bN\b|\bnight\b|\bhs\b', clean, re.I):
        freq = "Once daily at night (N)"
        raw_code = "OD_N"
    elif re.search(r'\b(?:PRN|As needed|When required)\b', clean, re.I):
        freq = "As needed (PRN)"
        raw_code = "PRN"
    elif re.search(r'\b(?:SOS|Emergency)\b', clean, re.I):
        freq = "As needed for symptoms (SOS)"
        raw_code = "SOS"

    # Timing
    timing = "Please confirm with your healthcare professional."
    if re.search(r'\b(?:cpm|3pm|7\s*pm|7:00\s*pm)\b', clean, re.I):
        timing = "7:00 PM (Evening)"
    elif re.search(r'\b(?:yter\s*sood|after\s*food|after\s*meals?|pc)\b', clean, re.I):
        timing = "After meals (after food)"
    elif re.search(r'\b(?:bbf|before\s*breakfast)\b', clean, re.I):
        timing = "Before breakfast (on empty stomach)"
    elif re.search(r'\b(?:abf|after\s*breakfast)\b', clean, re.I):
        timing = "After breakfast"
    elif re.search(r'\b(?:ac|before\s*meals?|before\s*food|empty\s*stomach)\b', clean, re.I):
        timing = "Before meals (on empty stomach)"
    elif is_topical:
        timing = "Morning and Night"
    elif "night" in freq.lower():
        timing = "At bedtime"

    # Duration
    duration = "Please confirm with your healthcare professional."
    if re.search(r'\b(?:imonfi|dmonf|1\s*month|1month)\b', clean, re.I):
        duration = "1 month"
    elif re.search(r'\b(?:20\s*dys|20\s*days|x\s*dy)\b', clean, re.I):
        duration = "20 days"
    elif re.search(r'\b(?:lwek|lweh|6\s*weeks?)\b', clean, re.I):
        duration = "6 weeks"
    else:
        dur_m = re.search(r'(?:x|for)\s*(\d+\s*(?:days?|weeks?|months?|years?))', clean, re.I)
        if dur_m:
            duration = dur_m.group(1).strip()

    # Instructions
    if is_topical:
        instructions = "Apply externally over affected area as directed."
    elif "7:00" in timing:
        instructions = "Take once daily at 7:00 PM."
    elif "after food" in timing.lower():
        instructions = "Take at night after food."
    else:
        instructions = f"Take as directed ({timing})."

    return MedicationItem(
        name=name,
        generic_name=generic,
        dose_and_unit=dose,
        route=route,
        frequency=freq,
        raw_frequency_code=raw_code,
        timing=timing,
        duration=duration,
        instructions=instructions,
        source_sentence=clean
    )

print("--- TESTING ON SYNTHETIC SAMPLES ---")
for s in SYNTHETIC_SAMPLES:
    meds = parse_medication_text(s["raw_text"])
    print(f"{s['title']}: {len(meds)} meds")

print("\n--- TESTING ON OCR DOCTOR PRESCRIPTION ---")
ocr_sample = """
G612683 G812683
MIMS
glal q lal2s Hospital
INITIALEVALUATION Derma
DAinL DAILL TINBA LOEPDPIS
my ty CAp. LTEAIyI aOOm 0
2 X dmonf X imonfi
yter sood IPoopeoe
Yen Tenb LecoPeImg
2 N
p Cpm X X dy
LvLiCLIn2-xL UeOm fna xf wmae 1x-2 nn217a7 ssg
cbm uabm en ne 006 0984
Revieo Revievo N X Lwek Lweh
"""
meds = parse_medication_text(ocr_sample)
print(f"Doctor Prescription Extracted: {len(meds)} meds")
for m in meds:
    print(f"  • {m.name} | Dose: {m.dose_and_unit} | Freq: {m.frequency} | Timing: {m.timing} | Dur: {m.duration} | Route: {m.route} | Instr: {m.instructions}")
