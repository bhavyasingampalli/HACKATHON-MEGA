"""
Medical Abbreviation Glossary for CareBridge AI.
Maps standard clinical abbreviations to patient-friendly explanations,
frequencies, timings, and routes.
"""

MEDICAL_ABBREVIATIONS = {
    # Frequencies
    "OD": {"meaning": "Once daily", "slots": ["morning"], "telugu": "రోజుకు ఒకసారి (ఉదయం)", "per_day": 1},
    "QD": {"meaning": "Once daily", "slots": ["morning"], "telugu": "రోజుకు ఒకసారి (ఉదయం)", "per_day": 1},
    "BD": {"meaning": "Twice daily", "slots": ["morning", "night"], "telugu": "రోజుకు రెండుసార్లు (ఉదయం మరియు రాత్రి)", "per_day": 2},
    "BID": {"meaning": "Twice daily", "slots": ["morning", "night"], "telugu": "రోజుకు రెండుసార్లు (ఉదయం మరియు రాత్రి)", "per_day": 2},
    "TDS": {"meaning": "Three times a day", "slots": ["morning", "afternoon", "night"], "telugu": "రోజుకు మూడుసార్లు (ఉదయం, మధ్యాహ్నం, రాత్రి)", "per_day": 3},
    "TID": {"meaning": "Three times a day", "slots": ["morning", "afternoon", "night"], "telugu": "రోజుకు మూడుసార్లు (ఉదయం, మధ్యాహ్నం, రాత్రి)", "per_day": 3},
    "QID": {"meaning": "Four times a day", "slots": ["morning", "afternoon", "evening", "night"], "telugu": "రోజుకు నాలుగుసార్లు", "per_day": 4},
    "Q4H": {"meaning": "Every 4 hours as needed/scheduled", "telugu": "ప్రతి 4 గంటలకు", "per_day": 6},
    "Q6H": {"meaning": "Every 6 hours", "telugu": "ప్రతి 6 గంటలకు", "per_day": 4},
    "Q8H": {"meaning": "Every 8 hours", "telugu": "ప్రతి 8 గంటలకు", "per_day": 3},
    "Q12H": {"meaning": "Every 12 hours", "telugu": "ప్రతి 12 గంటలకు", "per_day": 2},
    "PRN": {"meaning": "As needed (only when required)", "telugu": "అవసరమైనప్పుడు మాత్రమే", "per_day": 0},
    "SOS": {"meaning": "In emergency / As needed for symptoms", "telugu": "అత్యవసరమైనప్పుడు లేదా నొప్పి వచ్చినప్పుడు మాత్రమే", "per_day": 0},
    "STAT": {"meaning": "Immediately / Single dose only", "telugu": "వెంటనే ఒకేసారి", "per_day": 1},
    "HS": {"meaning": "At bedtime", "slots": ["night"], "telugu": "పడుకునే ముందు", "per_day": 1},
    "QHS": {"meaning": "Every night at bedtime", "slots": ["night"], "telugu": "ప్రతి రోజూ రాత్రి పడుకునే ముందు", "per_day": 1},
    "MANE": {"meaning": "In the morning", "slots": ["morning"], "telugu": "ఉదయం పూట", "per_day": 1},
    "NOCTE": {"meaning": "At night", "slots": ["night"], "telugu": "రాత్రి వేళ", "per_day": 1},
    
    # Timing relative to food
    "AC": {"meaning": "Before meals / Before food", "telugu": "భోజనానికి ముందు", "food_relation": "before_food"},
    "PC": {"meaning": "After meals / After food", "telugu": "భోజనం తర్వాత", "food_relation": "after_food"},
    "BBF": {"meaning": "Before breakfast", "telugu": "అల్పాహారానికి ముందు", "food_relation": "before_breakfast"},
    "ABF": {"meaning": "After breakfast", "telugu": "అల్పాహారం తర్వాత", "food_relation": "after_breakfast"},
    "WM": {"meaning": "With meals / With food", "telugu": "భోజనంతో పాటు", "food_relation": "with_food"},
    
    # Routes
    "PO": {"meaning": "By mouth (oral)", "telugu": "నోటి ద్వారా (మింగాలి)"},
    "SL": {"meaning": "Under the tongue (sublingual - do not swallow whole)", "telugu": "నాలుక కింద ఉంచాలి (మింగకూడదు)"},
    "SC": {"meaning": "Under the skin (subcutaneous injection)", "telugu": "చర్మం కింద సూది ద్వారా"},
    "IM": {"meaning": "Into muscle (intramuscular injection)", "telugu": "కండరాల సూది ద్వారా"},
    "IV": {"meaning": "Into vein (intravenous infusion)", "telugu": "నరాల ద్వారా"},
    "TOP": {"meaning": "Apply on skin (topical)", "telugu": "చర్మంపై పూయాలి"},
    "INH": {"meaning": "Inhalation (breathe in through mouth)", "telugu": "పీల్చడం ద్వారా"},
    
    # Dosage forms
    "TAB": {"meaning": "Tablet", "telugu": "మాత్ర (టాబ్లెట్)"},
    "CAP": {"meaning": "Capsule", "telugu": "క్యాప్సూల్"},
    "SYP": {"meaning": "Syrup / Liquid", "telugu": "సిరప్ (ద్రవ ఔషధం)"},
    "OINT": {"meaning": "Ointment", "telugu": "లేపనం"},
    "CREAM": {"meaning": "Cream", "telugu": "క్రీమ్"},
    "DROPS": {"meaning": "Drops", "telugu": "చుక్కల మందు"},
    "MDI": {"meaning": "Metered Dose Inhaler", "telugu": "ఇన్హేలర్"},
    
    # Clinical terms
    "BP": {"meaning": "Blood Pressure", "telugu": "రక్తపోటు (బ్లడ్ ప్రెజర్)"},
    "HR": {"meaning": "Heart Rate", "telugu": "గుండె వేగం"},
    "PR": {"meaning": "Pulse Rate", "telugu": "నాడి వేగం"},
    "RR": {"meaning": "Respiratory Rate", "telugu": "శ్వాస రేటు"},
    "SPO2": {"meaning": "Blood Oxygen Level", "telugu": "రక్తంలో ఆక్సిజన్ స్థాయి"},
    "FBS": {"meaning": "Fasting Blood Sugar", "telugu": "ఖాళీ కడుపున రక్తంలో చక్కెర"},
    "PPBS": {"meaning": "Post-Meal Blood Sugar", "telugu": "భోజనం తర్వాత రక్తంలో చక్కెర"},
    "RBS": {"meaning": "Random Blood Sugar", "telugu": "రక్తంలో చక్కెర స్థాయి"},
    "HBA1C": {"meaning": "3-Month Blood Sugar Average", "telugu": "3 నెలల సగటు చక్కెర పరీక్ష"},
    "OPD": {"meaning": "Outpatient Department / Clinic", "telugu": "ఔట్ పేషెంట్ క్లినిక్ (OPD)"},
    "IPD": {"meaning": "Inpatient Department", "telugu": "ఇన్ పేషెంట్ విభాగం"},
    "ICU": {"meaning": "Intensive Care Unit", "telugu": "తీవ్ర నిఘా విభాగం (ICU)"},
    "ER": {"meaning": "Emergency Room", "telugu": "అత్యవసర విభాగం (ఎమర్జెన్సీ వార్డు)"},
    "ED": {"meaning": "Emergency Department", "telugu": "అత్యవసర విభాగం"},
    "KFT": {"meaning": "Kidney Function Test", "telugu": "కిడ్నీ పనితీరు పరీక్ష"},
    "LFT": {"meaning": "Liver Function Test", "telugu": "కాలేయ పనితీరు పరీక్ష"},
    "CBC": {"meaning": "Complete Blood Count", "telugu": "సంపూర్ణ రక్త పరీక్ష"},
    "ECG": {"meaning": "Electrocardiogram (Heart check)", "telugu": "గుండె ఈసీజీ పరీక్ష"},
    "ECHO": {"meaning": "Echocardiogram (Heart Ultrasound)", "telugu": "గుండె అల్ట్రాసౌండ్ స్కానింగ్"},
    "CXR": {"meaning": "Chest X-Ray", "telugu": "ఛాతీ ఎక్స్-రే"},
    "USG": {"meaning": "Ultrasound Scan", "telugu": "అల్ట్రాసౌండ్ స్కానింగ్"},
}
