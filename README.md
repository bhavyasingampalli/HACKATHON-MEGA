# 🌉 CareBridge AI — Discharge Summary to Patient-Friendly Care Plan

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-teal.svg)](https://fastapi.tiangolo.com)
[![PyMuPDF](https://img.shields.io/badge/PDF_Extraction-PyMuPDF-green.svg)](https://pymupdf.readthedocs.io/)
[![Telugu](https://img.shields.io/badge/Bilingual-English_%26_తెలుగు-orange.svg)]()
[![Tests](https://img.shields.io/badge/Tests-27%2F27_Passing-brightgreen.svg)]()
[![Auth](https://img.shields.io/badge/Security-PBKDF2--SHA256_Auth-teal.svg)]()
[![Safety_Gate](https://img.shields.io/badge/Medical_Faithfulness-11--Point_Audit-red.svg)]()


> **"Understand Your Care. Recover With Confidence."**  
> Turn complex hospital discharge instructions into simple, bilingual, patient-friendly care plans for patients and families in English and Telugu.

---

## 🏥 1. Core Clinical Safety Directive

> **Medical faithfulness is more important than fluency. Never invent, omit, or alter clinical instructions.**

Discharge summaries communicate life-critical instructions: medication schedules, post-surgical precautions, dietary restrictions, and emergency red flags. When patients misunderstand these instructions due to Latin abbreviations (`BD`, `PC`, `PRN`, `HS`), complex medical jargon, or language barriers, the risk of adverse drug events and 30-day hospital readmissions rises dramatically.

**CareBridge AI is designed exclusively for communicating existing clinician-provided instructions—not diagnosing diseases or prescribing treatment.**

---

## ✨ 2. Key Features & Innovations

### 🛡️ A. 11-Point Medical Faithfulness Checker & Hard Safety Gate
An independent clinical verification module audits every generated care plan against original source clinical facts before display:
1. **Medication Completeness**: Verifies all source medications are represented.
2. **Dosage & Strength Verification**: Halts alterations (e.g. catches 500 mg $\to$ 5000 mg).
3. **Unit Preservation**: Validates measurement units (`mg`, `mcg`, `ml`, `puffs`).
4. **Frequency Fidelity**: Detects schedule tampering (e.g. twice daily $\to$ once daily).
5. **Route of Administration**: Enforces oral, sublingual, or inhaler routes.
6. **Treatment Duration**: Verifies course lengths and tapering schedules.
7. **Follow-Up Scheduling**: Preserves exact appointment dates, times, and OPD clinics.
8. **Emergency Warning Signs Recall**: Catches omitted red flags (hypoglycemia, chest pain, fever, bleeding).
9. **Diet & Activity Alignment**: Grounded strictly in explicit clinician instructions.
10. **Hallucination / Unsupported Instruction Shield**: Flags any unauthorized interventions.
11. **Telugu Cross-Language Clinical Verification**: Validates numbers, units, and drug names independently.

> **Hard Safety Gate:** If any discrepancy is detected, the care plan is immediately flagged as **`CLINICIAN REVIEW REQUIRED`** with verbatim source evidence cited. It is never silently marked as verified.

---

### 🇮🇳 B. Natural Telugu Localization (తెలుగు)
- Culturally authentic, natural Telugu script (`తెలుగు లిపి`).
- **Brand & Generic Protection**: Drug names are preserved in English alongside Telugu phonetic guides (`మెట్‌ఫార్మిన్ 500 మి.గ్రా.`) to prevent pharmacy dispense errors.
- Explains clinical timing relative to Indian dietary habits (e.g., *అల్పాహారానికి ముందు*, *భోజనం తర్వాత*).
- Interactive language tabs: **🇬🇧 English**, **🇮🇳 తెలుగు**, or **⚖️ Side-by-Side Bilingual**.

---

### 🧊 C. One-Page Printable Fridge Sheet
- Designed for refrigerator doors or medicine cabinets for daily tracking by older adults and family members.
- **Daily Adherence Checkboxes**: Morning, Noon, and Night tracking boxes for each medicine.
- **Emergency Alert Box**: High-visibility red banner with urgent warning signs and emergency actions.
- **Follow-up Date Banner**: Prominently highlights the next clinical review appointment.
- Available as a **downloadable PDF** (via ReportLab) and a **printable HTML view** (`@media print` on A4).

---

### 📅 D. Seven-Day Medicine Timetable
- Structured day-by-day pill schedule across 4 daily intervals:
  - 🌅 Morning (Breakfast)
  - ☀️ Afternoon (Lunch)
  - 🌆 Evening (Dinner)
  - 🌙 Bedtime (Night)
- **Draft Schedule Warnings**: If timing is not explicitly stated in the summary, items are marked in amber with clinician confirmation disclaimers.

---

### 🔊 E. Text-to-Speech (TTS) Voice Reader
- Built-in accessible voice reader using the Web Speech API.
- Reads verified care plans aloud in natural English (`en-US`) and Telugu (`te-IN`).
- Speed control (`0.8x`, `1.0x`, `1.2x`) for older adults.
- Never skips safety-critical emergency warning signs.

---

### 📖 F. Readability Scoring (Class 8 English Standard)
- **Flesch-Kincaid Grade Level**: Targets Class 7–8 English (Grade $\le 8.0$) for patient readability.
- **Flesch Reading Ease**: Measures syllable and sentence length balance.
- **Dravidian Linguistic Assessment**: Evaluates Telugu text with native script purity and sentence metrics (recognizing that English syllable formulas are invalid for agglutinative Dravidian languages).

---

### 📥 G. Scanned PDF Protection with PyMuPDF
- Extracts high-fidelity text from PDF discharge summaries using PyMuPDF (`fitz`).
- **Scanned Document Detection**: If a PDF is image-only with no readable text layer, CareBridge AI halts processing with clear guidance: *"Optical Character Recognition (OCR) is required. Never silently process unreadable documents."*

---

## 🧪 3. Synthetic Benchmark Dataset

CareBridge AI includes 5 pre-loaded synthetic clinical demo cases:
1. **Type 2 Diabetes & Essential Hypertension** (Metformin, Glimepiride, Telmisartan, Methylcobalamin, hypoglycemia emergency signs).
2. **Post-Operative Laparoscopic Cholecystectomy** (Cefuroxime, Pantoprazole, Paracetamol, Tramadol PRN, incision care, jaundice/fever red flags).
3. **Acute Coronary Syndrome (Post-MI / Stent)** (Aspirin, Clopidogrel, Atorvastatin, Metoprolol, Sublingual Sorbitrate PRN, cardiology OPD follow-up).
4. **Acute Asthma / COPD Exacerbation** (Inhaler Levosalbutamol + Ipratropium, Budesonide rotacaps, Prednisolone taper, SpO2 red flags).
5. **Postpartum Caesarean Section (Maternity)** (Cefixime, Diclofenac PRN, Iron, Calcium, lactation instructions, postpartum preeclampsia warnings).

---

## 🚀 4. Quick Start Guide

### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Modern Web Browser (Chrome, Edge, Firefox, Safari)

### Installation
```bash
# Clone or navigate to the repository
cd "Mega hackathon"

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Start the FastAPI dev server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Open your browser and navigate to: **`http://localhost:8000`**

---

## 📊 5. Automated Evaluation & Testing

### Run Pytest Test Suite (18 Automated Tests)
```bash
python -m pytest -p no:cacheprovider
```
Verifies medication extraction, dosage tampering detection, frequency fidelity, red-flag recall, Telugu fact preservation, readability scoring, and PDF extraction.

### Run Hackathon Evaluation Benchmark Harness (`evaluate.py`)
```bash
python evaluate.py
```
Outputs terminal evaluation results across all 5 clinical gold-standard cases and 2 adversarial error-injection tests (10x dose mutation and omitted emergency warnings):

```text
================================================================================
FINAL BENCHMARK EVALUATION SUMMARY:
  • Total Benchmark Samples: 5
  • Gold-Standard Verification Rate: 100.0%
  • Fact Preservation Rate: 100.0%
  • Adversarial Error Detection Rate: 100.0% (2 of 2 caught by Hard Safety Gate)
  • Average Readability: Grade 8.1 (Target Class 8: MET)
================================================================================
```

---

## 🛠️ 6. API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Web dashboard (protected route, redirects to `/login` if unauthenticated) |
| `GET` | `/login` | Clinical login & registration portal with teal/white theme |
| `POST` | `/api/auth/register` | Register new user with hashed passwords (PBKDF2-SHA256) |
| `POST` | `/api/auth/login` | Authenticate user & create secure session cookie |
| `POST` | `/api/auth/logout` | Terminate session & clear cookies |
| `GET` | `/api/auth/me` | Current authenticated user profile |
| `POST` | `/api/auth/forgot-password` | Generate 1-hour password reset token |
| `POST` | `/api/auth/reset-password` | Reset account password using token |
| `GET` | `/api/health` | Health check & model status |
| `GET` | `/api/demo-samples` | Fetches the 5 synthetic patient cases |
| `POST` | `/api/upload` | Accepts PDF/TXT with PyMuPDF extraction & scanned doc check |
| `POST` | `/api/generate` | Generates bilingual care plan with 11-point safety audit |
| `POST` | `/api/validate` | Independent Medical Faithfulness verification endpoint |
| `GET` | `/api/fridge-sheet` | Downloads 1-page A4 PDF or renders printable HTML |
| `GET` | `/api/history` | Lists historical care plans from SQLite |
| `GET` | `/api/dashboard-stats` | Aggregated safety metrics & preservation rates |
| `POST` | `/api/evaluate` | Runs automated benchmark evaluation suite |


---

## 🏛️ 7. Architecture & Technology Stack

```
Mega hackathon/
├── app/
│   ├── main.py                  # FastAPI server & route handlers
│   ├── config.py                # Environment configurations
│   ├── models/
│   │   └── schemas.py           # Pydantic schemas for data validation
│   ├── core/
│   │   ├── clinical_nlp.py      # Grounded clinical extraction engine
│   │   ├── faithfulness.py      # 11-point Medical Faithfulness Checker & Hard Safety Gate
│   │   ├── translator.py        # Telugu clinical translation & fact mapping
│   │   ├── readability.py       # Flesch-Kincaid & Telugu linguistic complexity metrics
│   │   ├── fridge_sheet.py      # Printable 1-page A4 PDF & HTML generator (ReportLab)
│   │   ├── timetable.py         # 7-day schedule generator with draft safety flags
│   │   ├── pdf_extractor.py     # PyMuPDF text extractor with scanned PDF rejection
│   │   ├── llm_service.py       # Unified LLM provider (Gemini / OpenAI / Fallback)
│   │   └── database.py          # SQLite persistence for previous reports & audits
│   ├── data/
│   │   ├── synthetic_samples.py # 5 gold-standard discharge summaries
│   │   ├── abbreviations.py     # Comprehensive medical abbreviation glossary
│   │   └── drug_reference.py    # Clinical drug dictionary
│   ├── static/
│   │   ├── css/style.css        # Accessible healthcare design system (teal & blue)
│   │   └── js/app.js            # Frontend logic, TTS reader, live audits, benchmarks
│   └── templates/
│       ├── index.html           # Healthcare dashboard single-page application
│       └── fridge_sheet.html    # A4 printable fridge sheet template
├── tests/
│   ├── test_extraction.py       # Medication & condition extraction tests
│   ├── test_faithfulness.py     # Faithfulness checker & safety gate tests
│   ├── test_readability.py      # Flesch-Kincaid & Telugu metrics tests
│   ├── test_pdf.py              # PyMuPDF & scanned PDF tests
│   └── test_api.py              # FastAPI endpoint tests
├── evaluate.py                  # Automated benchmark evaluation harness
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment configuration template
└── README.md                    # Project documentation
```

---

## ⚖️ 8. Medical & Legal Disclaimer

CareBridge AI is designed to improve health literacy and patient communication by summarizing and translating existing clinician-issued discharge instructions into plain language. It does not provide medical diagnosis, initiate treatment, or alter clinician orders. In all circumstances, original clinician-issued discharge instructions take precedence. If any instruction is ambiguous or contradicts physician advice, patients and family members must immediately consult their treating healthcare professional or contact emergency medical services.
