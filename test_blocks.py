import re
import difflib
from app.data.drug_reference import DRUG_REFERENCE, DRUG_ALIASES
from app.models.schemas import MedicationItem

SAMPLE_OCR_TEXT = """
G612683 G812683
MIMS
Hospital
INITIALEVALUATION Derma
DAinL DAILL TINBA LOEPDPIS
my ty CAp. LTAIyI abOm CAp. LTEAIyI aOOm 0
2 X dmonf X imonfi
yter sood IPoopeoe
Yen Tenb Lecopeamg LecoPeImg
2 N
p Cpm X X dy
LvLiCLIn2-xL UeOm fna xf wmae 1x-2 nn217a7 ssg
cbm uabm en ne 006 0984
Revieo Revievo N X Lwek Lweh
"""

def resolve_drug(name_raw: str):
    clean = re.sub(r'[^a-zA-Z0-9\s\-]', ' ', name_raw).strip().lower()
    tokens = [t for t in clean.split() if len(t) >= 3]
    for token in tokens:
        if token in DRUG_ALIASES:
            key = DRUG_ALIASES[token]
            return key, DRUG_REFERENCE[key]
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

def parse_blocks(text: str):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    blocks = []
    curr_lines = []
    
    for l in lines:
        is_med_start = False
        k, _ = resolve_drug(l)
        if k:
            is_med_start = True
        elif re.search(r'(?:^|\s)(?:Tab|Cap|Syp|Inj|Cream|Oint|Inhaler)\.?\b', l, re.I):
            is_med_start = True
            
        if is_med_start and curr_lines:
            blocks.append(' '.join(curr_lines))
            curr_lines = [l]
        elif curr_lines:
            if "revie" in l.lower() or "follow" in l.lower():
                blocks.append(' '.join(curr_lines))
                curr_lines = []
            else:
                curr_lines.append(l)
        elif is_med_start:
            curr_lines.append(l)
            
    if curr_lines:
        blocks.append(' '.join(curr_lines))
        
    return blocks

blocks = parse_blocks(SAMPLE_OCR_TEXT)
print(f"Detected {len(blocks)} medication blocks:")
for i, b in enumerate(blocks):
    print(f"Block {i+1}: {b}")
