"""
Fictional Synthetic Discharge Summaries for CareBridge AI Demo & Evaluation.
All patient data and hospital records are 100% synthetic and created for educational/demo testing.
"""

SYNTHETIC_SAMPLES = [
    {
        "id": "diabetes-hypertension",
        "title": "1. Type 2 Diabetes & Hypertension Care",
        "patient_name": "Ramesh Kumar (Demo Patient)",
        "condition": "Type 2 Diabetes Mellitus with Essential Hypertension",
        "category": "Endocrinology & Internal Medicine",
        "raw_text": """APOLLO HEALTHCARE NETWORK - DISCHARGE SUMMARY
PATIENT RECORD: #CB-90214 | ADMISSION DATE: 10-Oct-2026 | DISCHARGE DATE: 14-Oct-2026
PATIENT NAME: Ramesh Kumar | AGE: 56 Y | GENDER: Male | ATTENDING: Dr. K. S. Rao, MD (Int. Med.)

DIAGNOSIS ON DISCHARGE:
1. Uncontrolled Type 2 Diabetes Mellitus with symptomatic hyperglycemia (HbA1c: 9.4% on admission).
2. Essential Hypertension (Grade II).
3. Mild peripheral sensory neuropathy.

HOSPITAL COURSE:
Patient admitted with complaints of polyuria, polydipsia, and fatigue for 3 weeks. Blood sugars stabilized with insulin sliding scale and oral anti-diabetic agents. Pre-discharge fasting blood sugar: 126 mg/dL, Post-prandial blood sugar: 168 mg/dL. Blood pressure controlled at 128/82 mmHg.

DISCHARGE MEDICATIONS:
1. Tab. Metformin 500 mg - 1 tablet PO BD PC (Twice daily after food) x 30 days.
2. Tab. Glimepiride 1 mg - 1 tablet PO OD BBF (Once daily before breakfast) x 30 days.
3. Tab. Telmisartan 40 mg - 1 tablet PO OD MANE (Once daily in the morning) x 30 days.
4. Cap. Methylcobalamin 1500 mcg - 1 capsule PO OD HS (Once daily at bedtime) x 30 days.

DIETARY INSTRUCTIONS:
- Diabetic diet: Strictly avoid refined white sugar, sweets, carbonated beverages, and deep-fried items.
- Low-sodium diet: Restrict daily salt intake to less than 5 grams per day. Avoid pickles, papads, and canned foods.
- High-fiber meals: Eat whole grains (millets, brown rice), green leafy vegetables, and whole pulses.

ACTIVITY & LIFESTYLE:
- Moderate brisk walking for 30 minutes daily, 5 days per week. Avoid high-impact jumping exercises.
- Diabetic foot care: Inspect feet daily for cuts, blisters, redness, or peeling skin. Always wear protective, well-fitted footwear even indoors.

EMERGENCY WARNING SIGNS (RED FLAGS):
- Symptoms of hypoglycemia (low blood sugar): sudden cold sweating, trembling/shakiness, extreme hunger, dizziness, confusion, or blurred vision. If blood sugar is below 70 mg/dL, immediately consume 15 grams of fast-acting glucose (such as 3 teaspoons of sugar or half a glass of fruit juice) and repeat sugar test after 15 minutes.
- Severe persistent headache, vision changes, or chest tightness.
- Non-healing foot sores or fever with chills.
Proceed to the nearest Emergency Department immediately if symptoms do not resolve.

FOLLOW-UP APPOINTMENT:
- Review on 28-Oct-2026 at 10:30 AM with Dr. K. S. Rao at Room 204, Outpatient Department (OPD).
- Bring fasting blood sugar and post-lunch blood sugar log for 7 consecutive days.
- Repeat serum creatinine and electrolytes before follow-up visit.
"""
    },
    {
        "id": "post-op-cholecystectomy",
        "title": "2. Post-Operative Laparoscopic Cholecystectomy",
        "patient_name": "Sunita Devi (Demo Patient)",
        "condition": "Symptomatic Cholelithiasis (Gallbladder Stone Removal)",
        "category": "General & Laparoscopic Surgery",
        "raw_text": """METROPOLITAN SURGICAL HOSPITAL - DISCHARGE SUMMARY
PATIENT RECORD: #MSH-4821 | ADMISSION DATE: 11-Oct-2026 | DISCHARGE DATE: 13-Oct-2026
PATIENT NAME: Sunita Devi | AGE: 42 Y | GENDER: Female | SURGEON: Dr. Aruna Sharma, MS (Gen Surg)

PROCEDURE PERFORMED:
Elective 4-Port Laparoscopic Cholecystectomy under General Anesthesia on 11-Oct-2026.
Findings: Chronically inflamed gall bladder with multiple calculi (largest 14 mm). Uneventful removal, subhepatic drain removed on post-op day 1.

DISCHARGE MEDICATIONS:
1. Tab. Cefuroxime Axetil 500 mg - 1 tablet PO BD PC (Twice daily after food) x 5 days.
2. Tab. Pantoprazole 40 mg - 1 tablet PO OD BBF (Once daily before breakfast on empty stomach) x 7 days.
3. Tab. Paracetamol 650 mg - 1 tablet PO TDS (Three times a day) x 3 days.
4. Tab. Tramadol 50 mg - 1 tablet PO SOS (Take 1 tablet only for severe break-through pain, maximum 2 tablets per 24 hours).
5. Syp. Lactulose 15 ml - PO HS PRN (At bedtime as needed if constipated).

WOUND & INCISION CARE:
- Keep the umbilical and abdominal puncture sites clean and dry.
- Waterproof surgical dressings can remain in place for 5 days. Do not scrub or pick at the surgical glue or steri-strips.
- Sponge bath permitted; avoid submerging in bathtub or swimming pool until incision heals completely.

DIET & RECOVERY RESTRICTIONS:
- Low-fat, bland diet for the first 2 to 3 weeks. Limit heavy cream, fried foods, and rich gravies to avoid loose stools and bloating.
- Small, frequent meals (5 to 6 small meals a day).
- Physical activity: Light walking encouraged immediately to prevent blood clots. Avoid lifting heavy objects (>5 kg) or doing strenuous abdominal exercises for 4 weeks.

EMERGENCY WARNING SIGNS (RED FLAGS):
- High-grade fever greater than 100.4 F (38 C) with chills.
- Progressive abdominal distension, severe persistent belly pain not relieved by medication, or repeated vomiting.
- Yellowing of the eyes or skin (jaundice) or dark brownish urine.
- Redness, severe warmth, foul-smelling discharge, or active bleeding from the umbilical incision site.
If any of these signs develop, contact the surgical on-call registrar or report to Hospital Emergency Room immediately.

FOLLOW-UP APPOINTMENT:
- Suture and wound check on 20-Oct-2026 at 11:00 AM with Dr. Aruna Sharma, Surgical OPD Clinic 3.
- Histopathology report review during the same visit.
"""
    },
    {
        "id": "cardiac-post-mi",
        "title": "3. Acute Coronary Syndrome (Post-Myocardial Infarction)",
        "patient_name": "Venkat Raman (Demo Patient)",
        "condition": "Acute Inferior Wall Myocardial Infarction / Post-PCI Stent",
        "category": "Interventional Cardiology",
        "raw_text": """GLOBAL INSTITUTE OF CARDIOLOGY - DISCHARGE SUMMARY
PATIENT RECORD: #GIC-77301 | ADMISSION DATE: 08-Oct-2026 | DISCHARGE DATE: 13-Oct-2026
PATIENT NAME: Venkat Raman | AGE: 61 Y | GENDER: Male | CARDIOLOGIST: Dr. M. V. Prasad, DM (Cardiology)

CLINICAL SUMMARY:
Admitted with acute crushing retrosternal chest pain radiating to left arm with diaphoresis. ECG showed ST-elevation in II, III, aVF. Primary Percutaneous Coronary Intervention (PCI) performed on 08-Oct-2026: Successful drug-eluting stent (DES) deployed to Right Coronary Artery (RCA) with TIMI-3 flow. Echo on discharge: LVEF 48%, mild inferior wall hypokinesia.

DISCHARGE MEDICATIONS:
1. Tab. Aspirin 75 mg (Ecosprin) - 1 tablet PO OD PC (Once daily after lunch) x lifelong.
2. Tab. Clopidogrel 75 mg - 1 tablet PO OD PC (Once daily after lunch) x 12 months.
3. Tab. Atorvastatin 40 mg - 1 tablet PO OD HS (Once daily at bedtime) x ongoing.
4. Tab. Metoprolol Succinate 25 mg - 1 tablet PO BD PC (Twice daily after food) x ongoing.
5. Tab. Ramipril 2.5 mg - 1 tablet PO OD MANE (Once daily in the morning) x ongoing.
6. Tab. Sorbitrate (Isosorbide Dinitrate) 5 mg - 1 tablet Sublingual SL SOS for acute chest pain. Place under tongue; do not swallow.

DIETARY & CARDIAC REHABILITATION:
- Strictly low-salt (less than 3 grams sodium/day), low-cholesterol, heart-healthy Mediterranean-style diet.
- Total fluid intake restricted to 1.5 to 1.8 liters in 24 hours.
- Absolute smoking and tobacco cessation. Avoid passive secondhand smoke.
- Supervised cardiac walking: 15 to 20 minutes flat-ground walk twice daily. Avoid climbing steep stairs quickly, heavy lifting, or straining.

EMERGENCY WARNING SIGNS (RED FLAGS):
- Recurrent chest pain, heaviness, tightness, or burning radiating to jaw, neck, back, or left arm lasting longer than 5 minutes.
- If chest pain occurs: Sit down immediately and place 1 tablet of Sorbitrate 5 mg under your tongue. If pain does not subside within 5 minutes, DO NOT WAIT — call emergency ambulance (108 / 112) or go to the nearest Emergency Cardiac Center immediately.
- Sudden severe shortness of breath, inability to lie flat, or coughing pink frothy sputum.
- Sudden dizziness, blackouts, fainting spells, or pulse rate falling below 50 beats per minute or exceeding 110 beats per minute.

FOLLOW-UP APPOINTMENT:
- Cardiology Review on 24-Oct-2026 at 09:30 AM with Dr. M. V. Prasad, Cardiac Science Wing, Room 102.
- Bring ECG, Blood Pressure chart (recorded twice daily for 7 days), and Serum Lipid Profile & KFT reports.
"""
    },
    {
        "id": "respiratory-asthma-copd",
        "title": "4. Acute Exacerbation of Bronchial Asthma / COPD",
        "patient_name": "Lakshmi Narayana (Demo Patient)",
        "condition": "Severe Acute Exacerbation of Bronchial Asthma",
        "category": "Pulmonology & Respiratory Medicine",
        "raw_text": """PULMONARY CARE & CHEST HOSPITAL - DISCHARGE SUMMARY
PATIENT RECORD: #PCH-3310 | ADMISSION DATE: 09-Oct-2026 | DISCHARGE DATE: 12-Oct-2026
PATIENT NAME: Lakshmi Narayana | AGE: 49 Y | GENDER: Male | PULMONOLOGIST: Dr. S. Sudhakar, MD (Pulm)

CLINICAL PROFILE:
Known asthmatic for 8 years, presented with acute onset severe breathlessness, wheezing, and productive cough triggered by viral upper respiratory infection. Oxygen saturation at presentation was 88% on room air. Treated with nebulized bronchodilators, intravenous steroids, and oxygen therapy. Discharged in stable condition with SpO2 96% on room air and clear lung fields.

DISCHARGE MEDICATIONS:
1. Inhaler Levosalbutamol + Ipratropium (50 mcg + 20 mcg) MDI with Spacer - 2 puffs INH TDS (Three times a day) x 7 days, then PRN for wheezing.
2. Rotacap Budesonide 200 mcg - 1 capsule INH BD via Rotahaler (Twice daily morning and night) x ongoing. (Rinse mouth with water after use).
3. Tab. Prednisolone 20 mg - 1 tablet PO OD BBF in morning with food x 5 days, then taper to 10 mg OD x 3 days, then stop.
4. Tab. Azithromycin 500 mg - 1 tablet PO OD PC (Once daily 1 hour after lunch) x 3 days.
5. Tab. Montelukast 10 mg - 1 tablet PO OD HS (Once daily at bedtime) x 30 days.

HOME CARE & ENVIRONMENTAL PRECAUTIONS:
- Inhaler technique: Always use a spacer device with the metered-dose inhaler. Inhale slowly and deeply, and hold breath for 10 seconds.
- Mouth rinse: Rinse mouth thoroughly and gargle with lukewarm water after using Budesonide rotacap to prevent throat hoarseness or oral fungal infections (thrush).
- Environmental control: Strictly avoid dust, pet dander, incense smoke (agarbatti), mosquito coils, aerosol sprays, and sudden exposure to chilled air or cold drinks.
- Daily steam inhalation twice daily for 5 minutes.

EMERGENCY WARNING SIGNS (RED FLAGS):
- Severe breathlessness where you cannot speak full sentences without pausing for breath.
- Fingernails or lips turning bluish or pale.
- Blood oxygen saturation (SpO2) measured on home pulse oximeter drops below 92%.
- No relief 15 minutes after taking 2 to 4 rescue puffs of Levosalbutamol inhaler.
- High fever (>101 F) with foul-smelling rusty or dark green phlegm.
If any red flag occurs, report to the Emergency Department immediately or call ambulance.

FOLLOW-UP APPOINTMENT:
- Pulmonology Clinic review on 21-Oct-2026 at 02:00 PM with Dr. S. Sudhakar, Chest Clinic OPD Counter 4.
- Spirometry (Pulmonary Function Test) scheduled 1 hour before appointment at 01:00 PM.
"""
    },
    {
        "id": "maternity-caesarean-care",
        "title": "5. Postpartum Care (Lower Segment Caesarean Section)",
        "patient_name": "Priyanka Reddy (Demo Patient)",
        "condition": "Full-Term Primigravida Post Lower Segment Caesarean Section (LSCS)",
        "category": "Obstetrics & Gynecology",
        "raw_text": """WOMEN & CHILD MATERNITY HOSPITAL - DISCHARGE SUMMARY
PATIENT RECORD: #WCH-5592 | ADMISSION DATE: 10-Oct-2026 | DISCHARGE DATE: 14-Oct-2026
PATIENT NAME: Priyanka Reddy | AGE: 28 Y | GENDER: Female | OBSTETRICIAN: Dr. Radha Madhavi, MD, DGO

DELIVERY DETAILS:
Delivered healthy baby boy (birth weight: 3.2 kg, APGAR 9/10) via emergency LSCS indicated for non-reassuring fetal heart tones on 10-Oct-2026 under spinal anesthesia. Uterus well contracted, lochia rubra moderate, incision clean. Mother and baby healthy and bonding well. Baby receiving exclusive breastfeeding.

DISCHARGE MEDICATIONS:
1. Tab. Cefixime 200 mg - 1 tablet PO BD PC (Twice daily after food) x 5 days.
2. Tab. Diclofenac Potassium 50 mg - 1 tablet PO BD PC PRN (Twice daily after meals only for incision pain) x 3 days.
3. Tab. Pantoprazole 40 mg - 1 tablet PO OD BBF (Once daily before breakfast) x 5 days.
4. Tab. Ferrous Ascorbate + Folic Acid (Iron) - 1 tablet PO OD PC (Once daily after lunch with citrus juice or water) x 90 days.
5. Tab. Calcium Carbonate 500 mg with Vitamin D3 - 1 tablet PO BD PC (Twice daily after food) x 90 days. (Note: maintain 2-hour gap from Iron tablet).

BREASTFEEDING & MATERNAL CARE:
- Exclusive breastfeeding on baby demand (every 2 to 3 hours). Ensure proper latching covering the entire areola to avoid cracked nipples.
- Incision care: Keep the bikini-line surgical incision clean and dry. Avoid tight elastic waistbands directly pressing on the wound.
- Perineal hygiene: Change sanitary pads frequently (at least every 3 to 4 hours).
- Pelvic rest: No vaginal douching, tampons, or sexual intercourse for 6 weeks.
- Nutrition: High-protein, nutrient-rich meals, plenty of fluids (warm water, soups, milk) at least 3 liters daily.

EMERGENCY WARNING SIGNS (RED FLAGS):
- Abnormally heavy vaginal bleeding: soaking more than one large sanitary pad within an hour, or passing large blood clots larger than a golf ball.
- High fever exceeding 100.4 F (38 C), chills, or foul-smelling vaginal discharge.
- Severe pain, redness, spreading warmth, or pus oozing from the abdominal incision site.
- Severe throbbing headache, sudden visual disturbances, or upper right belly pain (warning signs of postpartum preeclampsia).
- Pain, swelling, or redness in one calf (warning sign of deep vein thrombosis / DVT).
- Persistent overwhelming sadness, severe anxiety, crying spells, or thoughts of harming self or newborn (postpartum depression/psychosis).
Seek urgent medical attention at the Maternal Emergency Triage if any warning signs occur.

FOLLOW-UP APPOINTMENT:
- Suture removal / incision check on 22-Oct-2026 at 10:00 AM with Dr. Radha Madhavi at Room 12, GYN OPD.
- Pediatric well-baby checkup and vaccination for newborn on 24-Oct-2026 with Dr. Ananya (Pediatrics).
"""
    }
]
