import re
import difflib
from app.data.drug_reference import DRUG_REFERENCE, DRUG_ALIASES

def resolve_drug(name_raw: str):
    clean = re.sub(r'[^a-zA-Z0-9\s\-]', ' ', name_raw).strip().lower()
    tokens = [t for t in clean.split() if len(t) >= 3]
    
    # 1. Exact match on token or alias
    for token in tokens:
        if token in DRUG_ALIASES:
            key = DRUG_ALIASES[token]
            return key, DRUG_REFERENCE[key]
        if token in DRUG_REFERENCE:
            return token, DRUG_REFERENCE[token]
            
    # 2. Check compound / multi-word matches
    for alias, target in DRUG_ALIASES.items():
        if alias in clean:
            return target, DRUG_REFERENCE[target]
            
    # 3. Fuzzy similarity on tokens >= 4 chars
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

test_inputs = [
    "1) CAp. LTEAIyI aOOm N (after food) x 1 month",
    "2) Tenb Lecopeamg N (7pm) X dy",
    "3) LvLiCLIn2-xL UeOm for external application over affected area M N x 6 weeks"
]

for t in test_inputs:
    key, data = resolve_drug(t)
    print(t, "->", key, data["generic"] if data else None)
