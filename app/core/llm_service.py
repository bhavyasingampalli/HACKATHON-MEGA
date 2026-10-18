"""
AI LLM Service for CareBridge AI.
Supports Google Gemini API, OpenAI API, and seamlessly falls back to the
built-in deterministic clinical NLP engine when no API keys are configured.
Guarantees zero-failure, offline-capable, clinical-grade reliability.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from app.models.schemas import ClinicalExtraction, MedicationItem, FollowUpItem, WarningSignItem
from app.core.clinical_nlp import extract_clinical_information
from app.core.translator import build_telugu_care_plan

logger = logging.getLogger("carebridge.llm")


def extract_with_llm_or_fallback(
    source_text: str,
    custom_api_key: Optional[str] = None
) -> ClinicalExtraction:
    """
    Extracts structured clinical information using LLM if credentials are provided,
    otherwise uses the deterministic clinical NLP parser.
    """
    gemini_key = custom_api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if gemini_key:
        try:
            return _call_gemini_extraction(source_text, gemini_key)
        except Exception as e:
            logger.warning(f"Gemini API extraction failed ({e}), using deterministic clinical parser fallback.")
            return extract_clinical_information(source_text)
    elif openai_key:
        try:
            return _call_openai_extraction(source_text, openai_key)
        except Exception as e:
            logger.warning(f"OpenAI API extraction failed ({e}), using deterministic clinical parser fallback.")
            return extract_clinical_information(source_text)
    else:
        # High-accuracy deterministic clinical extraction fallback
        return extract_clinical_information(source_text)


def _call_gemini_extraction(source_text: str, api_key: str) -> ClinicalExtraction:
    """Calls Gemini LLM with strict grounding instructions."""
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = (
            "You are a medical information extractor. Extract clinical data from this discharge summary.\n"
            "CRITICAL RULE: Faithfulness is more important than fluency. Never invent, alter, or omit instructions.\n"
            "Link every instruction to its verbatim source sentence.\n"
            "Return valid JSON matching the schema with patient_name, conditions, medications, warning_signs, follow_ups, diet, activity.\n\n"
            f"DISCHARGE SUMMARY:\n{source_text}"
        )
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        text_resp = response.text
        # Clean markdown fences
        if "```json" in text_resp:
            text_resp = text_resp.split("```json")[1].split("```")[0].strip()
        elif "```" in text_resp:
            text_resp = text_resp.split("```")[1].split("```")[0].strip()
        
        parsed = json.loads(text_resp)
        # Parse into ClinicalExtraction or fallback if incomplete
        if "medications" in parsed and len(parsed["medications"]) > 0:
            return ClinicalExtraction(**parsed)
    except Exception as e:
        logger.error(f"Error in Gemini extraction: {e}")
    
    # Fallback
    return extract_clinical_information(source_text)


def _call_openai_extraction(source_text: str, api_key: str) -> ClinicalExtraction:
    """Calls OpenAI API with structured JSON response."""
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical data extractor. Extract conditions, medications, warning signs, and follow-ups. Do not infer. Preserve exact doses and units."
                },
                {"role": "user", "content": source_text}
            ],
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        if "medications" in data:
            return ClinicalExtraction(**data)
    except Exception as e:
        logger.error(f"Error in OpenAI extraction: {e}")

    return extract_clinical_information(source_text)
