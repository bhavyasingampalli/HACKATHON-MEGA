"""
Drug Reference Database for CareBridge AI.
Maps common discharge medications to generic names, therapeutic purpose,
and plain-language explanations in English and Telugu.
"""

DRUG_REFERENCE = {
    # Diabetic Medications
    "metformin": {
        "generic": "Metformin Hydrochloride",
        "category": "Anti-diabetic",
        "purpose_en": "Controls blood sugar levels by helping your body use insulin better.",
        "purpose_te": "రక్తంలో చక్కెర స్థాయిని నియంత్రించడంలో సహాయపడుతుంది.",
        "cautions_en": "Take with meals to reduce stomach upset. Do not skip meals.",
        "cautions_te": "కడుపు నొప్పి రాకుండా భోజనంతో పాటు తీసుకోవాలి."
    },
    "glimepiride": {
        "generic": "Glimepiride",
        "category": "Anti-diabetic (Sulfonylurea)",
        "purpose_en": "Helps your pancreas produce more insulin to lower blood sugar.",
        "purpose_te": "రక్తంలో షుగర్ తగ్గించడానికి ఇన్సులిన్ ఉత్పత్తికి సహాయపడుతుంది.",
        "cautions_en": "Take just before breakfast. Keep fast-acting sugar or candy handy in case of low blood sugar.",
        "cautions_te": "అల్పాహారానికి ముందు తీసుకోవాలి. షుగర్ తగ్గితే తీపి లేదా చాక్లెట్ దగ్గర ఉంచుకోండి."
    },
    "sitagliptin": {
        "generic": "Sitagliptin",
        "category": "Anti-diabetic (DPP-4 inhibitor)",
        "purpose_en": "Increases insulin release after meals and decreases sugar made by liver.",
        "purpose_te": "భోజనం తర్వాత చక్కెరను అదుపులో ఉంచుతుంది.",
        "cautions_en": "Can be taken with or without food.",
        "cautions_te": "ఆహారంతో లేదా ఆహారం లేకుండా తీసుకోవచ్చు."
    },
    "empagliflozin": {
        "generic": "Empagliflozin",
        "category": "Anti-diabetic (SGLT-2 inhibitor)",
        "purpose_en": "Helps kidneys remove excess sugar through urine and protects the heart.",
        "purpose_te": "మూత్రం ద్వారా అదనపు చక్కెరను తొలగించి గుండెను రక్షిస్తుంది.",
        "cautions_en": "Drink plenty of water throughout the day to avoid dehydration.",
        "cautions_te": "రోజు మొత్తం పుష్కలంగా నీరు త్రాగాలి."
    },

    # Cardiovascular Medications
    "telmisartan": {
        "generic": "Telmisartan",
        "category": "Anti-hypertensive (ARB)",
        "purpose_en": "Relaxes blood vessels to lower blood pressure and protect kidneys.",
        "purpose_te": "రక్తపోటును (BP) తగ్గించడానికి రక్తనాళాలను విశ్రాంతి పరుస్తుంది.",
        "cautions_en": "Take at the same time every day. Stand up slowly from sitting or lying down.",
        "cautions_te": "ప్రతిరోజూ ఒకే సమయానికి తీసుకోవాలి."
    },
    "amlodipine": {
        "generic": "Amlodipine Besylate",
        "category": "Anti-hypertensive (Calcium channel blocker)",
        "purpose_en": "Lowers blood pressure and relieves chest discomfort by relaxing arteries.",
        "purpose_te": "రక్తపోటును నియంత్రించి గుండెకు రక్తప్రసరణను సులభతరం చేస్తుంది.",
        "cautions_en": "Report ankle or foot swelling if it occurs.",
        "cautions_te": "పాదాల వాపు వస్తే వైద్యుడికి తెలియజేయండి."
    },
    "metoprolol": {
        "generic": "Metoprolol Succinate / Tartrate",
        "category": "Beta-blocker",
        "purpose_en": "Slows heart rate and reduces workload on the heart.",
        "purpose_te": "గుండె కొట్టుకునే వేగాన్ని మరియు శ్రమను తగ్గిస్తుంది.",
        "cautions_en": "Do not stop taking this medication suddenly without doctor guidance.",
        "cautions_te": "వైద్యుడిని సంప్రదించకుండా అకస్మాత్తుగా ఆపకూడదు."
    },
    "aspirin": {
        "generic": "Aspirin (Acetylsalicylic Acid)",
        "category": "Antiplatelet / Blood thinner",
        "purpose_en": "Prevents blood clots from forming in heart and brain vessels.",
        "purpose_te": "రక్తం గడ్డకట్టకుండా కాపాడి గుండెపోటును నివారిస్తుంది.",
        "cautions_en": "Take after meals. Watch for unusual bruising or bleeding.",
        "cautions_te": "భోజనం తర్వాత తీసుకోవాలి. రక్తస్రావం గమనించండి."
    },
    "clopidogrel": {
        "generic": "Clopidogrel Bisulfate",
        "category": "Antiplatelet",
        "purpose_en": "Prevents platelets from clumping together to prevent clots in stents or arteries.",
        "purpose_te": "రక్తనాళాలలో మరియు స్టెంట్లలో రక్తం గడ్డకట్టకుండా అడ్డుకుంటుంది.",
        "cautions_en": "Do not skip doses. Inform dentists or surgeons that you are on this medicine.",
        "cautions_te": "రోజూ క్రమం తప్పకుండా తీసుకోవాలి."
    },
    "atorvastatin": {
        "generic": "Atorvastatin Calcium",
        "category": "Cholesterol-lowering (Statin)",
        "purpose_en": "Lowers bad LDL cholesterol and stabilizes plaque in blood vessels.",
        "purpose_te": "చెడు కొలెస్ట్రాల్‌ను తగ్గించి గుండె జబ్బుల ముప్పును తగ్గిస్తుంది.",
        "cautions_en": "Usually taken at bedtime. Report unexplained muscle aches.",
        "cautions_te": "రాత్రి పడుకునే ముందు తీసుకోవడం మంచిది."
    },
    "nitroglycerin": {
        "generic": "Nitroglycerin / Glyceryl Trinitrate / Sorbitrate",
        "category": "Nitrate vasodilator",
        "purpose_en": "Quickly opens heart blood vessels to relieve sudden chest tightness or pain.",
        "purpose_te": "ఛాతీ నొప్పి వచ్చినప్పుడు గుండె రక్తనాళాలను తక్షణమే తెరుస్తుంది.",
        "cautions_en": "Place under tongue, DO NOT swallow. Sit down before taking as it may cause dizziness.",
        "cautions_te": "నాలుక కింద ఉంచాలి, మింగకూడదు. తీసుకునేటప్పుడు కూర్చోవాలి."
    },
    "sorbitrate": {
        "generic": "Isosorbide Dinitrate",
        "category": "Nitrate vasodilator",
        "purpose_en": "Relieves sudden heart pain (angina) by expanding heart arteries.",
        "purpose_te": "ఛాతీ నొప్పి సమయంలో ఉపశమనం కోసం నాలుక కింద ఉంచే మాత్ర.",
        "cautions_en": "Place under the tongue. Seek emergency care if pain persists after 5 minutes.",
        "cautions_te": "నాలుక కింద ఉంచండి. 5 నిమిషాల తర్వాత కూడా నొప్పి తగ్గకపోతే వెంటనే ఆసుపత్రికి వెళ్ళండి."
    },

    # Post-operative & Antibiotics
    "cefuroxime": {
        "generic": "Cefuroxime Axetil",
        "category": "Antibiotic (Cephalosporin)",
        "purpose_en": "Treats or prevents bacterial infections following surgery.",
        "purpose_te": "శస్త్రచికిత్స తర్వాత బాక్టీరియల్ ఇన్ఫెక్షన్లను నివారిస్తుంది.",
        "cautions_en": "Complete the full prescribed course even if you feel better.",
        "cautions_te": "నయం అయినట్లు అనిపించినా డాక్టర్ సూచించిన మొత్తం రోజులు వాడాలి."
    },
    "cefixime": {
        "generic": "Cefixime",
        "category": "Antibiotic (Cephalosporin)",
        "purpose_en": "Prevents and treats bacterial infections after childbirth or procedures.",
        "purpose_te": "బాక్టీరియా వల్ల వచ్చే ఇన్ఫెక్షన్లను నయం చేస్తుంది.",
        "cautions_en": "Complete the full course as prescribed.",
        "cautions_te": "మొత్తం కోర్సు పూర్తి చేయాలి."
    },
    "amoxicillin": {
        "generic": "Amoxicillin / Clavulanate",
        "category": "Antibiotic (Penicillin class)",
        "purpose_en": "Antibiotic for bacterial infections of respiratory tract, skin, or surgery.",
        "purpose_te": "బ్యాక్టీరియా ఇన్ఫెక్షన్లను నియంత్రించే యాంటీబయాటిక్.",
        "cautions_en": "Take with meals. Complete all prescribed doses.",
        "cautions_te": "భోజనంతో పాటు తీసుకోవాలి."
    },
    "azithromycin": {
        "generic": "Azithromycin",
        "category": "Antibiotic (Macrolide)",
        "purpose_en": "Fights respiratory bacterial infections.",
        "purpose_te": "శ్వాసకోశ ఇన్ఫెక్షన్లను నివారించే యాంటీబయాటిక్.",
        "cautions_en": "Take 1 hour before or 2 hours after meals with water.",
        "cautions_te": "భోజనానికి 1 గంట ముందు లేదా 2 గంటల తర్వాత తీసుకోవాలి."
    },
    "pantoprazole": {
        "generic": "Pantoprazole Sodium",
        "category": "Proton Pump Inhibitor (Antacid)",
        "purpose_en": "Protects the stomach lining from acid and reduces nausea/heartburn.",
        "purpose_te": "కడుపులో ఎసిడిటీ, గ్యాస్ మరియు మంటను నివారిస్తుంది.",
        "cautions_en": "Take in the morning on an empty stomach, 30 minutes before breakfast.",
        "cautions_te": "ఉదయం ఖాళీ కడుపుతో, టిఫిన్‌కు 30 నిమిషాల ముందు వేసుకోవాలి."
    },
    "paracetamol": {
        "generic": "Paracetamol / Acetaminophen",
        "category": "Analgesic & Antipyretic",
        "purpose_en": "Relieves mild to moderate pain and reduces fever.",
        "purpose_te": "శరీర నొప్పులు మరియు జ్వరాన్ని తగ్గిస్తుంది.",
        "cautions_en": "Do not exceed 4,000 mg in 24 hours. Take with plenty of water.",
        "cautions_te": "రోజుకు నిర్ణీత పరిమాణం కంటే ఎక్కువ తీసుకోకూడదు."
    },
    "tramadol": {
        "generic": "Tramadol Hydrochloride",
        "category": "Moderate Opioid Analgesic",
        "purpose_en": "Relieves severe post-surgical pain when regular painkillers are not enough.",
        "purpose_te": "తీవ్రమైన శస్త్రచికిత్స అనంతర నొప్పి నివారణకు.",
        "cautions_en": "Take only when pain is severe (SOS). May cause drowsiness; avoid driving.",
        "cautions_te": "తీవ్రమైన నొప్పి ఉన్నప్పుడు మాత్రమే వేసుకోవాలి. నిద్రమత్తు రావచ్చు."
    },
    "diclofenac": {
        "generic": "Diclofenac Potassium / Sodium",
        "category": "NSAID Painkiller & Anti-inflammatory",
        "purpose_en": "Relieves surgical swelling, inflammation, and cramping pain.",
        "purpose_te": "నొప్పి మరియు వాపును తగ్గిస్తుంది.",
        "cautions_en": "Always take after food to protect your stomach.",
        "cautions_te": "కడుపులో మంట రాకుండా ఎల్లప్పుడూ భోజనం తర్వాతే తీసుకోవాలి."
    },

    # Respiratory Medications
    "budesonide": {
        "generic": "Budesonide",
        "category": "Inhaled Corticosteroid",
        "purpose_en": "Reduces swelling and inflammation inside your airways to prevent asthma attacks.",
        "purpose_te": "ఊపిరితిత్తులలో వాపును తగ్గించి ఆయాసాన్ని నివారిస్తుంది.",
        "cautions_en": "Rinse your mouth thoroughly with water and spit it out after every inhalation.",
        "cautions_te": "ఇన్హేలర్ వాడిన తర్వాత నోటిని నీటితో పుక్కిలించి ఉమ్మివేయాలి."
    },
    "levosalbutamol": {
        "generic": "Levosalbutamol / Levalbuterol",
        "category": "Short-acting Bronchodilator",
        "purpose_en": "Relaxes airway muscles to rapidly relieve chest tightness and breathlessness.",
        "purpose_te": "శ్వాసనాళాలను వెడల్పు చేసి శ్వాస సులభంగా ఆడేలా చేస్తుంది.",
        "cautions_en": "Use as directed. Shake inhaler well before each use.",
        "cautions_te": "వాడే ముందు ఇన్హేలర్‌ను బాగా కదిలించాలి."
    },
    "ipratropium": {
        "generic": "Ipratropium Bromide",
        "category": "Anticholinergic Bronchodilator",
        "purpose_en": "Opens airways and reduces mucous secretion in asthma/COPD.",
        "purpose_te": "శ్వాసకోశ మార్గాలను తెరచి కఫాన్ని నియంత్రిస్తుంది.",
        "cautions_en": "Avoid spraying near or into the eyes.",
        "cautions_te": "మందు కళ్లలో పడకుండా జాగ్రత్త వహించండి."
    },
    "prednisolone": {
        "generic": "Prednisolone",
        "category": "Oral Corticosteroid",
        "purpose_en": "Potent anti-inflammatory medicine to quickly calm severe lung inflammation.",
        "purpose_te": "తీవ్రమైన శ్వాసకోశ వాపును వేగంగా తగ్గించే స్టెరాయిడ్ ఔషధం.",
        "cautions_en": "Take in the morning with food. Strictly follow tapering schedule; do not stop abruptly.",
        "cautions_te": "ఉదయం భోజనంతో తీసుకోవాలి. డాక్టర్ చెప్పినట్లుగా మోతాదు క్రమంగా తగ్గించాలి."
    },

    # Maternity Care
    "iron": {
        "generic": "Ferrous Ascorbate / Folic Acid",
        "category": "Nutritional Supplement / Hematinic",
        "purpose_en": "Builds healthy red blood cells to treat or prevent postpartum anemia.",
        "purpose_te": "రక్తహీనతను నివారించి శరీరానికి రక్తం పట్టేలా చేస్తుంది.",
        "cautions_en": "Do not take at the exact same time as calcium or tea/coffee. Stools may turn dark.",
        "cautions_te": "కాల్షియం మాత్రతో లేదా టీ/కాఫీతో కలిపి తీసుకోకూడదు. మలవిసర్జన నల్లగా రావచ్చు."
    },
    "calcium": {
        "generic": "Calcium Carbonate + Vitamin D3",
        "category": "Mineral Supplement",
        "purpose_en": "Replenishes bone calcium and supports healthy breastmilk production.",
        "purpose_te": "ఎముకల బలానికి మరియు తల్లిపాలలో కాల్షియం కోసం.",
        "cautions_en": "Take after food with plenty of water. Keep 2 hours gap from iron supplements.",
        "cautions_te": "ఐరన్ మాత్రకు, ఈ కాల్షియం మాత్రకు మధ్య కనీసం 2 గంటల వ్యవధి ఉండాలి."
    },
    "methylcobalamin": {
        "generic": "Methylcobalamin (Vitamin B12)",
        "category": "Neurotropic Vitamin Supplement",
        "purpose_en": "Supports nerve health, treats peripheral neuropathy, and aids red blood cell production.",
        "purpose_te": "నరాల బలహీనతను నివారించి, విటమిన్ బి12 లోపాన్ని సరిచేస్తుంది.",
        "cautions_en": "Take with meals or at bedtime as prescribed.",
        "cautions_te": "డాక్టర్ సూచించినట్లు రాత్రి పూట లేదా భోజనంతో తీసుకోవాలి."
    },

    # Antifungal & Dermatology Medications
    "itrasys": {
        "generic": "Itraconazole",
        "category": "Oral Antifungal (Triazole)",
        "default_dose": "200 mg",
        "purpose_en": "Treats fungal skin and nail infections (such as Tinea Corporis / ringworm) by eradicating the fungal organism.",
        "purpose_te": "శిలీంధ్ర (ఫంగల్) చర్మ వ్యాధులు, తామర మరియు ఇన్ఫెక్షన్లను నయం చేస్తుంది.",
        "cautions_en": "Take with or immediately after a full meal (after food) for best absorption. Complete the full prescribed course.",
        "cautions_te": "మందు బాగా పనిచేయడానికి భోజనం తర్వాత వెంటనే తీసుకోవాలి. పూర్తి కోర్సు వాడాలి."
    },
    "itraconazole": {
        "generic": "Itraconazole",
        "category": "Oral Antifungal (Triazole)",
        "default_dose": "200 mg",
        "purpose_en": "Treats fungal skin and nail infections by stopping fungal cell growth.",
        "purpose_te": "ఫంగల్ ఇన్ఫెక్షన్లను అరికట్టే యాంటీఫంగల్ ఔషధం.",
        "cautions_en": "Take after meals (after food) with a full glass of water. Do not skip doses.",
        "cautions_te": "భోజనం తర్వాత నీటితో తీసుకోవాలి."
    },
    "lecope": {
        "generic": "Levocetirizine Hydrochloride",
        "category": "Antihistamine / Anti-allergy",
        "default_dose": "5 mg",
        "purpose_en": "Relieves skin itching, redness, hives, and allergic swelling.",
        "purpose_te": "చర్మ దురద, దద్దుర్లు మరియు అలెర్జీ సమస్యల నుండి ఉపశమనం కలిగిస్తుంది.",
        "cautions_en": "Take once daily in the evening (e.g. 7 PM or night). May cause mild drowsiness.",
        "cautions_te": "సాయంత్రం (ఉదా. రాత్రి 7 గంటలకు) లేదా రాత్రి పడుకునే ముందు తీసుకోవాలి. నిద్రమత్తు రావచ్చు."
    },
    "levocetirizine": {
        "generic": "Levocetirizine Hydrochloride",
        "category": "Antihistamine / Anti-allergy",
        "default_dose": "5 mg",
        "purpose_en": "Controls allergic reactions, skin itching, and watery eyes.",
        "purpose_te": "అలెర్జీ మరియు దురదను తగ్గించే మాత్ర.",
        "cautions_en": "Usually taken in the evening or at night. Avoid alcohol while taking this medicine.",
        "cautions_te": "సాయంత్రం లేదా రాత్రి తీసుకోవాలి."
    },
    "luliclinz": {
        "generic": "Luliconazole Cream 1% w/w",
        "category": "Topical Antifungal Cream",
        "default_dose": "Apply as directed (Thin layer)",
        "purpose_en": "Clears fungal skin infections (ringworm/tinea corporis) by eliminating fungal growth on skin.",
        "purpose_te": "చర్మంపై ఉండే తామర మరియు ఫంగస్ ఇన్ఫెక్షన్‌ను నివారించే పైపూత మందు.",
        "cautions_en": "For external application only. Apply gently over affected area as directed. Wash hands before and after.",
        "cautions_te": "చర్మంపై పైపూతగా మాత్రమే రాయాలి. ప్రభావిత ప్రాంతంపై పలుచగా రాయాలి. చేతులు కడుక్కోవాలి."
    },
    "luliconazole": {
        "generic": "Luliconazole Cream 1% w/w",
        "category": "Topical Antifungal Cream",
        "default_dose": "Apply as directed (Thin layer)",
        "purpose_en": "Treats ringworm (tinea corporis), jock itch, and athlete's foot.",
        "purpose_te": "ఫంగల్ ఇన్ఫెక్షన్ల నివారణకు వాడే పైపూత క్రీమ్.",
        "cautions_en": "Clean and dry the affected area before applying. Do not apply near eyes or mouth.",
        "cautions_te": "శుభ్రమైన చర్మంపై మాత్రమే రాయాలి."
    },
    "terbinafine": {
        "generic": "Terbinafine Hydrochloride",
        "category": "Antifungal",
        "default_dose": "250 mg",
        "purpose_en": "Treats stubborn fungal infections of the skin, body, and nails.",
        "purpose_te": "మొండి ఫంగల్ మరియు చర్మ ఇన్ఫెక్షన్లను నయం చేస్తుంది.",
        "cautions_en": "Take once daily. Complete the full prescribed course.",
        "cautions_te": "రోజుకు ఒకసారి తీసుకోవాలి. కోర్సు పూర్తి చేయాలి."
    },
    "ketoconazole": {
        "generic": "Ketoconazole",
        "category": "Antifungal",
        "default_dose": "2% Cream / 200 mg",
        "purpose_en": "Treats fungal skin infections and dandruff.",
        "purpose_te": "చర్మం మరియు తలలో ఫంగస్ ఇన్ఫెక్షన్లను తగ్గిస్తుంది.",
        "cautions_en": "Use as directed by your dermatologist.",
        "cautions_te": "వైద్యుడు సూచించినట్లు వాడాలి."
    },
    "clotrimazole": {
        "generic": "Clotrimazole",
        "category": "Antifungal (Topical)",
        "default_dose": "1% Cream",
        "purpose_en": "Treats fungal skin infections including ringworm and sweat rash.",
        "purpose_te": "తామర మరియు చెమట కాయలు/ఫంగస్ నివారిణి.",
        "cautions_en": "Apply a thin layer to the affected area 2 to 3 times daily.",
        "cautions_te": "ప్రభావిత ప్రాంతంపై పలుచగా రాయాలి."
    },
    "fluconazole": {
        "generic": "Fluconazole",
        "category": "Antifungal",
        "default_dose": "150 mg",
        "purpose_en": "Treats internal and fungal skin infections.",
        "purpose_te": "ఫంగల్ ఇన్ఫెక్షన్లను నయం చేసే యాంటీఫంగల్ టాబ్లెట్.",
        "cautions_en": "Take as prescribed, usually once a week or as directed.",
        "cautions_te": "వైద్యుల సూచన మేరకు వాడాలి."
    },
    "cetirizine": {
        "generic": "Cetirizine Hydrochloride",
        "category": "Antihistamine",
        "default_dose": "10 mg",
        "purpose_en": "Relieves allergy symptoms like itching, runny nose, and hives.",
        "purpose_te": "దురద, తుమ్ములు మరియు అలెర్జీని తగ్గిస్తుంది.",
        "cautions_en": "May cause drowsiness; best taken at bedtime.",
        "cautions_te": "రాత్రి పడుకునే ముందు తీసుకోవడం మంచిది."
    },
    "fexofenadine": {
        "generic": "Fexofenadine Hydrochloride",
        "category": "Non-drowsy Antihistamine",
        "default_dose": "120 mg",
        "purpose_en": "Relieves allergic itching and hives without causing significant drowsiness.",
        "purpose_te": "నిద్రమత్తు లేకుండా అలెర్జీ మరియు దురదను తగ్గిస్తుంది.",
        "cautions_en": "Take with water. Avoid fruit juices within 2 hours of taking.",
        "cautions_te": "నీటితో తీసుకోవాలి. పండ్ల రసాలు మానుకోవాలి."
    }
}

# OCR / Handwriting Aliases for common medications and misspellings
DRUG_ALIASES = {
    # Itrasys / Itraconazole variants
    "itrasys": "itrasys",
    "itrasys 200": "itrasys",
    "itrasys 200mg": "itrasys",
    "ltrays": "itrasys",
    "ltraays": "itrasys",
    "lteaiyi": "itrasys",
    "ltaiys": "itrasys",
    "itrays": "itrasys",
    "itrasis": "itrasys",
    "itraconazole": "itraconazole",

    # Lecope / Levocetirizine variants
    "lecope": "lecope",
    "lecope 5": "lecope",
    "lecope 5mg": "lecope",
    "lecopem": "lecope",
    "lecop": "lecope",
    "lecopa": "lecope",
    "lecopeamg": "lecope",
    "lecopeimg": "lecope",
    "levocetirizine": "levocetirizine",

    # Luliclinz / Luliconazole variants
    "luliclinz": "luliclinz",
    "luliclinz-xl": "luliclinz",
    "luliclinz xl": "luliclinz",
    "lvliclinz": "luliclinz",
    "lvliclinz-xl": "luliclinz",
    "luliclin": "luliclinz",
    "luliconazole": "luliconazole",
}

