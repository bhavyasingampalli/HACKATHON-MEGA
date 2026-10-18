"""
Pydantic Data Schemas for CareBridge AI.
Defines models for clinical information extraction, care plan generation,
faithfulness verification, readability analysis, and API contracts.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class MedicationItem(BaseModel):
    name: str = Field(..., description="Medication brand or generic name")
    generic_name: Optional[str] = Field(None, description="Generic formulation if available")
    dose_and_unit: str = Field(..., description="Dose quantity and unit (e.g. 500 mg, 2 puffs)")
    strength_value: Optional[float] = Field(None, description="Numeric strength value for faithfulness checking")
    strength_unit: Optional[str] = Field(None, description="Unit of measurement (mg, mcg, ml, etc.)")
    route: str = Field("Oral (by mouth)", description="Route of administration")
    frequency: str = Field(..., description="Frequency of intake (e.g. Twice daily, Once daily)")
    raw_frequency_code: Optional[str] = Field(None, description="Original code such as OD, BD, TDS, PRN")
    timing: str = Field("Please confirm with your healthcare professional.", description="Timing relative to meals or time of day")
    duration: str = Field("Please confirm with your healthcare professional.", description="Treatment duration")
    start_stop_dates: Optional[str] = Field(None, description="Explicit start or stop dates if stated")
    instructions: str = Field("", description="Specific instructions from the source text")
    source_sentence: str = Field(..., description="Verbatim text quote from the original discharge summary")
    telugu: Optional[Dict[str, str]] = Field(default_factory=dict, description="Telugu translated fields")


class FollowUpItem(BaseModel):
    date: str = Field(..., description="Appointment date")
    time: Optional[str] = Field(None, description="Appointment time")
    clinician_or_department: str = Field(..., description="Department or Doctor name")
    instructions: str = Field("", description="Required preparations, test reports to bring")
    source_sentence: str = Field(..., description="Source text sentence")
    telugu: Optional[Dict[str, str]] = Field(default_factory=dict)


class WarningSignItem(BaseModel):
    sign: str = Field(..., description="Emergency symptom or red flag")
    action: str = Field("Seek immediate medical care or visit the Emergency Department.", description="Immediate action needed")
    urgency: str = Field("EMERGENCY", description="Urgency level: EMERGENCY or HIGH")
    source_sentence: str = Field(..., description="Source sentence verifying this warning sign")
    telugu: Optional[Dict[str, str]] = Field(default_factory=dict)


class ClinicalExtraction(BaseModel):
    patient_name: Optional[str] = None
    patient_age: Optional[str] = None
    patient_gender: Optional[str] = None
    admission_date: Optional[str] = None
    discharge_date: Optional[str] = None
    conditions: List[str] = Field(default_factory=list)
    medications: List[MedicationItem] = Field(default_factory=list)
    warning_signs: List[WarningSignItem] = Field(default_factory=list)
    diet_instructions: List[str] = Field(default_factory=list)
    activity_restrictions: List[str] = Field(default_factory=list)
    wound_care_instructions: List[str] = Field(default_factory=list)
    other_instructions: List[str] = Field(default_factory=list)
    follow_ups: List[FollowUpItem] = Field(default_factory=list)
    raw_source_text: str = ""


class FaithfulnessCheckItem(BaseModel):
    category: str = Field(..., description="Category being verified")
    status: str = Field(..., description="PASS, FAIL, or REVIEW_REQUIRED")
    details: str = Field(..., description="Clinical verification summary")
    source_evidence: Optional[str] = None
    output_representation: Optional[str] = None
    discrepancy: Optional[str] = None


class FaithfulnessReport(BaseModel):
    overall_status: str = Field(..., description="VERIFIED or CLINICIAN_REVIEW_REQUIRED")
    passed_checks: int = 0
    failed_checks: int = 0
    review_needed_checks: int = 0
    checks: List[FaithfulnessCheckItem] = Field(default_factory=list)
    hard_safety_gate_triggered: bool = False
    safety_gate_message: str = ""
    metrics: Dict[str, float] = Field(default_factory=dict)


class ReadabilityReport(BaseModel):
    english: Dict[str, Any] = Field(default_factory=dict)
    telugu: Dict[str, Any] = Field(default_factory=dict)
    disclaimer: str = (
        "Readability formulas are mathematical estimates of sentence and syllable length, "
        "not definitive clinical proof that an individual patient understands the instructions. "
        "Always confirm critical care steps with your healthcare team."
    )


class CarePlanResponse(BaseModel):
    id: str
    patient_name: str
    condition: str
    extraction: ClinicalExtraction
    english_plan: Dict[str, Any]
    telugu_plan: Dict[str, Any]
    faithfulness_report: FaithfulnessReport
    readability: ReadabilityReport
    has_timetable: bool = False
    timetable: Optional[Dict[str, Any]] = None
    created_at: str


class GenerateRequest(BaseModel):
    text: str
    languages: List[str] = ["en", "te"]
    api_key: Optional[str] = None


class ValidateRequest(BaseModel):
    source_text: str
    english_plan: Dict[str, Any]
    telugu_plan: Optional[Dict[str, Any]] = None


class EvaluationBenchmarkResult(BaseModel):
    total_samples: int
    medication_preservation_rate: float
    dose_accuracy_rate: float
    frequency_accuracy_rate: float
    warning_recall_rate: float
    unsupported_instruction_count: int
    safety_gate_trigger_rate: float
    sample_reports: List[Dict[str, Any]]


class AssistantChatRequest(BaseModel):
    message: str = Field(..., description="User voice or text question")
    language: str = Field("en", description="Language code: en, te, hi, ta")
    plan_id: Optional[str] = Field(None, description="Optional active care plan ID")
    context: Optional[Dict[str, Any]] = Field(None, description="Active care plan context")
    api_key: Optional[str] = Field(None, description="Optional Gemini or OpenAI API key")


class AssistantChatResponse(BaseModel):
    reply: str
    language: str
    language_name: str
    voice_lang_code: str
    suggested_questions: List[str] = Field(default_factory=list)
    safety_disclaimer: str


class UserRegisterRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Account password (min 8 characters)")
    confirm_password: str = Field(..., description="Password confirmation")
    full_name: str = Field(..., min_length=2, description="User full name")
    role: str = Field("Clinician / Doctor", description="Clinical or patient role")


class UserLoginRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")
    remember_me: bool = Field(False, description="Remember login session")


class ForgotPasswordRequest(BaseModel):
    email: str = Field(..., description="Registered email address")


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., description="Password reset verification token")
    new_password: str = Field(..., min_length=8, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")


class UserProfileResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    created_at: str


class AuthResponse(BaseModel):
    success: bool
    message: str
    user: Optional[UserProfileResponse] = None
    token: Optional[str] = None


class UpdateProfileRequest(BaseModel):
    full_name: str = Field(..., min_length=2, description="Updated full name")



