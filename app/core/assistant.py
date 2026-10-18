"""
AI Voice Assistant Engine for CareBridge AI.
Supports English, Telugu (తెలుగు), Hindi (हिन्दी), and Tamil (தமிழ்).
Answers patient and family questions about their discharge summary,
medication timings, dietary rules, emergency signs, and follow-up care.
"""

import os
import re
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger("carebridge.assistant")

LANGUAGE_VOICE_CODES = {
    "en": "en-US",
    "te": "te-IN",
    "hi": "hi-IN",
    "ta": "ta-IN"
}

LANGUAGE_NAMES = {
    "en": "English",
    "te": "Telugu (తెలుగు)",
    "hi": "Hindi (हिन्दी)",
    "ta": "Tamil (தமிழ்)"
}

# Quick suggested questions in each language
SUGGESTED_QUESTIONS = {
    "en": [
        "When should I take my medicines?",
        "What are the emergency warning signs?",
        "What food should I eat or avoid?",
        "When is my follow-up appointment?",
        "Can I walk or do heavy work?"
    ],
    "te": [
        "నా మందులు ఎప్పుడు వేసుకోవాలి?",
        "అత్యవసర హెచ్చరిక లక్షణాలు ఏమిటి?",
        "నేను ఎలాంటి ఆహారం తీసుకోవాలి?",
        "నా తదుపరి డాక్టర్ అపాయింట్‌మెంట్ ఎప్పుడు?",
        "నేను నడవవచ్చా లేదా విశ్రాంతి తీసుకోవాలా?"
    ],
    "hi": [
        "मुझे अपनी दवाएं कब लेनी चाहिए?",
        "आपातकालीन खतरे के लक्षण क्या हैं?",
        "मुझे क्या खाना चाहिए और क्या नहीं?",
        "मेरा अगला डॉक्टर चेकअप कब है?",
        "क्या मैं पैदल चल सकता हूँ या काम कर सकता हूँ?"
    ],
    "ta": [
        "நான் மருந்துகளை எப்போது சாப்பிட வேண்டும்?",
        "அவசர எச்சரிக்கை அறிகுறிகள் என்ன?",
        "நான் என்ன உணவு சாப்பிட வேண்டும்?",
        "எனது அடுத்த மருத்துவ சந்திப்பு எப்போது?",
        "நான் நடக்கலாமா அல்லது ஓய்வெடுக்க வேண்டுமா?"
    ]
}


def build_context_prompt(care_plan_context: Optional[Dict[str, Any]]) -> str:
    """Builds a grounded medical summary context string from patient care plan."""
    if not care_plan_context:
        return "No specific patient care plan is loaded. Provide general, safe recovery guidance."

    overview = care_plan_context.get("patient_overview", {})
    patient_name = overview.get("patient_name", "Patient")
    conditions = overview.get("conditions", [])
    meds = care_plan_context.get("medicines", [])
    warnings = care_plan_context.get("warning_signs", [])
    diet = care_plan_context.get("diet_instructions", [])
    activity = care_plan_context.get("activity_restrictions", [])
    follow_ups = care_plan_context.get("follow_ups", [])

    lines = [
        f"PATIENT: {patient_name}",
        f"CONDITIONS: {', '.join(conditions) if isinstance(conditions, list) else conditions}",
        "PRESCRIBED MEDICINES:"
    ]
    for m in meds:
        lines.append(f" - {m.get('name')}: Dose: {m.get('dose_and_unit')}, Freq: {m.get('frequency')}, Timing: {m.get('timing')}, Route: {m.get('route')}, Duration: {m.get('duration')}. Instructions: {m.get('instructions')}")

    lines.append("EMERGENCY WARNING SIGNS (RED FLAGS):")
    for w in warnings:
        lines.append(f" - {w.get('sign')}: Action: {w.get('action')}")

    lines.append("DIET & NUTRITION:")
    for d in diet:
        lines.append(f" - {d}")

    lines.append("ACTIVITY & REST:")
    for a in activity:
        lines.append(f" - {a}")

    lines.append("FOLLOW-UP APPOINTMENTS:")
    for f in follow_ups:
        lines.append(f" - {f.get('date')} {f.get('time', '')} with {f.get('clinician_or_department')}: {f.get('instructions')}")

    return "\n".join(lines)


def query_llm_assistant(
    user_message: str,
    language: str,
    context_text: str,
    api_key: Optional[str] = None
) -> Optional[str]:
    """Queries Gemini or OpenAI LLM with strict medical grounding and native language output."""
    gemini_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    lang_name = LANGUAGE_NAMES.get(language, "English")

    system_instruction = (
        f"You are the CareBridge AI Voice Assistant for patients and family members.\n"
        f"Respond in {lang_name} using natural, patient-friendly phrasing suitable for older adults (Class 8 level).\n"
        f"STRICT CLINICAL RULES:\n"
        f"1. Medical faithfulness is paramount: Answer only using the provided patient discharge context.\n"
        f"2. Never invent dosages, extra medicines, or diagnosis.\n"
        f"3. If asked about emergency red flags (chest pain, breathlessness, heavy bleeding, fever, low blood sugar), emphasize immediate emergency care (call 108 / 112 or visit Emergency).\n"
        f"4. Keep spoken responses clear, warm, and concise (2 to 4 sentences) so it sounds natural when spoken aloud.\n\n"
        f"PATIENT DISCHARGE CONTEXT:\n{context_text}"
    )

    if gemini_key:
        try:
            from google import genai
            client = genai.Client(api_key=gemini_key)
            prompt = f"{system_instruction}\n\nUSER QUESTION: {user_message}\n\nANSWER IN {lang_name}:"
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            if response.text and response.text.strip():
                return response.text.strip()
        except Exception as e:
            logger.warning(f"Gemini API assistant call failed: {e}")

    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            import openai
            client = openai.OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=300
            )
            reply = response.choices[0].message.content.strip()
            if reply:
                return reply
        except Exception as e:
            logger.warning(f"OpenAI API assistant call failed: {e}")

    return None


def fallback_assistant_engine(
    user_message: str,
    language: str,
    care_plan_context: Optional[Dict[str, Any]]
) -> str:
    """
    Rich, rule-based multilingual clinical QA engine.
    Ensures 100% offline functionality in Telugu, Hindi, Tamil, and English.
    """
    msg_lower = user_message.lower().strip()
    lang = language.lower()
    
    meds = care_plan_context.get("medicines", []) if care_plan_context else []
    warnings = care_plan_context.get("warning_signs", []) if care_plan_context else []
    diet = care_plan_context.get("diet_instructions", []) if care_plan_context else []
    activity = care_plan_context.get("activity_restrictions", []) if care_plan_context else []
    follow_ups = care_plan_context.get("follow_ups", []) if care_plan_context else []
    patient_name = care_plan_context.get("patient_overview", {}).get("patient_name", "Patient") if care_plan_context else "Patient"

    # Identify question intent
    is_med_timing = any(w in msg_lower for w in [
        "medicine", "medication", "tablet", "dose", "when", "timing", "how to take",
        "మందు", "టాబ్లెట్", "ఎప్పుడు", "వేసుకోవాలి", "మోతాదు",
        "दवा", "गोली", "कब", "लेनी", "खुराक",
        "மருந்து", "மாத்திரை", "எப்போது", "சாப்பிட"
    ])

    is_warning = any(w in msg_lower for w in [
        "warning", "emergency", "danger", "red flag", "fever", "chest pain", "pain", "sugar", "bleeding", "hypo",
        "హెచ్చరిక", "అత్యవసరం", "ప్రమాదం", "నొప్పి", "ఛాతీ", "జ్వరం", "రక్తస్రావం",
        "खतरा", "आपातकालीन", "लक्षण", "दर्द", "सीने में दर्द", "बुखार",
        "எச்சரிக்கை", "அவசரம்", "வலி", "மார்பு வலி", "காய்ச்சல்", "இரத்தப்போக்கு"
    ])

    is_diet = any(w in msg_lower for w in [
        "diet", "food", "eat", "avoid", "water", "sugar", "salt",
        "ఆహారం", "తినాలి", "తినకూడదు", "ఉప్పు", "చక్కెర", "భోజనం",
        "खाना", "आहार", "नमक", "मीठा", "भोजन", "पानी",
        "உணவு", "சாப்பிட", "உப்பு", "சர்க்கரை", "சாப்பாடு"
    ])

    is_follow_up = any(w in msg_lower for w in [
        "follow up", "appointment", "doctor", "visit", "date", "when to meet",
        "అపాయింట్‌మెంట్", "డాక్టర్", "సందర్శన", "తేదీ", "ఎప్పుడు కలవాలి",
        "चेकअप", "डॉक्टर", "तारीख", "कब मिलना है", "अपॉइंटमेंट",
        "சந்திப்பு", "மருத்துவர்", "தேதி", "எப்போது பார்க்க வேண்டும்"
    ])

    is_activity = any(w in msg_lower for w in [
        "walk", "exercise", "rest", "heavy", "lift", "work",
        "నడవ", "వ్యాయామం", "విశ్రాంతి", "బరువు", "పని",
        "टहलना", "व्यायाम", "आराम", "भारी", "काम",
        "நடக்க", "உடற்பயிற்சி", "ஓய்வு", "பளு", "வேலை"
    ])

    # 1. Medication Question
    if is_med_timing:
        if meds:
            med_summaries = []
            for m in meds[:3]:
                med_summaries.append(f"{m.get('name')}: {m.get('dose_and_unit')}, {m.get('frequency')} ({m.get('timing')})")
            joined = "; ".join(med_summaries)

            if lang == "te":
                return f"{patient_name} గారి మందుల వివరాలు: {joined}. డాక్టర్ సూచించిన వేళలకు సరిగ్గా వేసుకోండి. ఏవైనా సందేహాలుంటే మీ వైద్యుడిని సంప్రదించండి."
            elif lang == "hi":
                return f"{patient_name} जी के लिए दवाएं: {joined}। कृपया सभी दवाएं डॉक्टर के बताए समय पर ही लें। खुद से कोई बदलाव न करें।"
            elif lang == "ta":
                return f"{patient_name} அவர்களுக்கான மருந்துகள்: {joined}. மருத்துவர் கூறிய நேரத்தில் சரியாக சாப்பிடுங்கள்."
            else:
                return f"Here are the prescribed medicines for {patient_name}: {joined}. Take each medicine exactly as scheduled with meals or water as directed."
        else:
            if lang == "te":
                return "దయచేసి మీ డిశ్చార్జ్ సారాంశాన్ని అప్‌లోడ్ చేయండి. మీ మందుల వివరాలను చూసి సరైన సమాధానం చెబుతాను."
            elif lang == "hi":
                return "कृपया अपना डिस्चार्ज सारांश अपलोड करें, ताकि मैं आपकी दवाओं की सही जानकारी दे सकूँ।"
            elif lang == "ta":
                return "உங்கள் டிஸ்சார்ஜ் ஆவணத்தை பதிவேற்றவும், மருந்துகள் பற்றி கூறுகிறேன்."
            else:
                return "Please upload your discharge summary so I can guide you on your specific medication schedule."

    # 2. Emergency Warning Question
    if is_warning:
        if warnings:
            w_list = [w.get("sign") for w in warnings[:3]]
            w_str = "; ".join(w_list)
            if lang == "te":
                return f"ముఖ్యమైన అత్యవసర సంకేతాలు: {w_str}। ఇటువంటి లక్షణాలు కనిపిస్తే వెంటనే అత్యవసర విభాగానికి (Emergency/108) వెళ్ళండి!"
            elif lang == "hi":
                return f"आपातकालीन खतरे के लक्षण: {w_str}। यदि इनमें से कोई भी लक्षण दिखे, तो तुरंत अस्पताल की इमरजेंसी में जाएं या 108 पर कॉल करें!"
            elif lang == "ta":
                return f"அவசர எச்சரிக்கை அறிகுறிகள்: {w_str}. இந்த அறிகுறிகள் இருந்தால் உடனடியாக அவசர சிகிச்சைப் பிரிவை அணுகவும் அல்லது 108 ஐ அழைக்கவும்!"
            else:
                return f"Emergency warning signs to watch for: {w_str}. If you notice any of these red flags, call emergency services (108/112) or go to the nearest Hospital Emergency Room immediately!"
        else:
            if lang == "te":
                return "తీవ్రమైన ఛాతీ నొప్పి, విపరీతమైన ఆయాసం, స్పృహ కోల్పోవడం లేదా ఆగని రక్తస్రావం ఉంటే వెంటనే 108 లేదా ఎమర్జెన్సీ విభాగానికి వెళ్ళండి."
            elif lang == "hi":
                return "यदि अचानक तेज सीने में दर्द, सांस लेने में तकलीफ या अत्यधिक रक्तस्राव हो, तो तुरंत इमरजेंसी (108) में संपर्क करें।"
            elif lang == "ta":
                return "கடுமையான மார்பு வலி அல்லது மூச்சுத்திணறல் ஏற்பட்டால் உடனே 108 அவசர சிகிச்சையை அழைக்கவும்."
            else:
                return "For any severe chest pain, shortness of breath, sudden weakness, or uncontrolled bleeding, seek emergency medical care immediately (call 108 or 112)."

    # 3. Diet Question
    if is_diet:
        if diet:
            d_str = "; ".join(diet[:3])
            if lang == "te":
                return f"ఆహార సూచనలు: {d_str}। తగినంత మంచినీరు త్రాగండి మరియు వైద్యులు నిషేధించిన ఆహారాన్ని మానుకోండి."
            elif lang == "hi":
                return f"खान-पान के निर्देश: {d_str}। पर्याप्त पानी पिएं और बाहर का या तला-भुना खाना न खाएं।"
            elif lang == "ta":
                return f"உணவு வழிகாட்டுதல்: {d_str}. காரம், எண்ணெய் பொருட்களை தவிர்த்து ஆரோக்கியமான உணவு உண்ணுங்கள்."
            else:
                return f"Your dietary recommendations: {d_str}. Drink plenty of clean water and avoid foods restricted by your doctor."
        else:
            if lang == "te":
                return "వైద్యులు సూచించిన తేలికపాటి, పౌష్టికాహారాన్ని మాత్రమే తీసుకోండి. ఉప్పు మరియు నూనె పదార్థాలు తగ్గించండి."
            elif lang == "hi":
                return "हल्का, सुपाच्य और पौष्टिक भोजन करें। ज्यादा नमक और चीनी से परहेज रखें।"
            elif lang == "ta":
                return "எளிதில் செரிமானமாகும் சத்தான உணவை உட்கொள்ளுங்கள். உப்பு குறைவாக சேர்க்கவும்."
            else:
                return "Eat light, nutritious meals as advised by your healthcare team. Keep salt, sugar, and oily foods low."

    # 4. Follow-up Question
    if is_follow_up:
        if follow_ups:
            f = follow_ups[0]
            f_str = f"{f.get('date')} {f.get('time', '')} with {f.get('clinician_or_department')}"
            if lang == "te":
                return f"మీ తదుపరి అపాయింట్‌మెంట్ తేదీ: {f_str}। మీ రక్త పరీక్షల రిపోర్టులను వెంట తీసుకువెళ్లండి."
            elif lang == "hi":
                return f"आपकी अगली डॉक्टर अपॉइंटमेंट: {f_str} है। अपने सभी पुराने टेस्ट और डिस्चार्ज पेपर साथ ले जाएं।"
            elif lang == "ta":
                return f"உங்கள் அடுத்த மருத்துவ சந்திப்பு: {f_str}. பழைய சிகிச்சை ஆவணங்களை உடன் எடுத்துச் செல்லவும்."
            else:
                return f"Your next follow-up appointment is on {f_str}. Remember to bring your prescription and previous test reports."
        else:
            if lang == "te":
                return "మీ డిశ్చార్జ్ పేపర్‌పై పేర్కొన్న తేదీ ప్రకారం లేదా సాధారణంగా 7 నుండి 10 రోజులలో డాక్టర్‌ను సంప్రదించండి."
            elif lang == "hi":
                return "डिस्चार्ज पेपर पर लिखी तारीख के अनुसार या 7-10 दिनों में अपने डॉक्टर से दोबारा मिलें।"
            elif lang == "ta":
                return "7 முதல் 10 நாட்களில் உங்கள் மருத்துவரை மீண்டும் சந்தித்து பரிசோதனை செய்யுங்கள்."
            else:
                return "Please check your discharge sheet or visit your clinician for a follow-up review within 7 to 10 days."

    # 5. Activity Question
    if is_activity:
        if activity:
            a_str = "; ".join(activity[:2])
            if lang == "te":
                return f"శారీరక శ్రమ మరియు విశ్రాంతి: {a_str}। బరువైన వస్తువులను ఎత్తవద్దు."
            elif lang == "hi":
                return f"गतिविधि और आराम: {a_str}। भारी वजन उठाने से बचें और पर्याप्त आराम करें।"
            elif lang == "ta":
                return f"ஓய்வு மற்றும் உடற்பயிற்சி: {a_str}. அதிக பளுவான பொருட்களை தூக்காதீர்கள்."
            else:
                return f"Activity guidelines: {a_str}. Avoid heavy lifting or strenuous activity until cleared by your physician."

    # General Greeting / Default Response
    if lang == "te":
        return f"నమస్కారం! నేను కేర్‌బ్రిడ్జ్ AI వాయిస్ అసిస్టెంట్‌ని. మీ మందుల సమయాలు, ఆహార నియమాలు, అత్యవసర హెచ్చరిక లక్షణాలు లేదా డాక్టర్ అపాయింట్‌మెంట్‌ల గురించి ఏవైనా అడగవచ్చు."
    elif lang == "hi":
        return f"नमस्ते! मैं केयरब्रिज AI वॉयस असिस्टेंट हूँ। आप अपनी दवाओं, खान-पान, खतरे के लक्षणों या डॉक्टर से मिलने के समय के बारे में मुझसे कोई भी सवाल पूछ सकते हैं।"
    elif lang == "ta":
        return f"வணக்கம்! நான் கேர்பிரிட்ஜ் AI குரல் உதவியாளர். உங்கள் மருந்துகள், உணவு முறைகள், எச்சரிக்கை அறிகுறிகள் குறித்து என்னிடம் எந்த கேள்வியும் கேட்கலாம்."
    else:
        return f"Hello! I am your CareBridge AI Voice Assistant. You can ask me about your medication schedule, food guidelines, emergency warning signs, or doctor follow-up appointments in any language."


def handle_assistant_interaction(
    message: str,
    language: str = "en",
    care_plan_context: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main dispatcher for the conversational Voice Assistant.
    Attempts LLM generation with fallback to offline multilingual medical engine.
    """
    lang_code = language.lower() if language else "en"
    if lang_code not in LANGUAGE_VOICE_CODES:
        lang_code = "en"

    voice_code = LANGUAGE_VOICE_CODES[lang_code]
    context_text = build_context_prompt(care_plan_context)

    # 1. Try LLM
    reply = query_llm_assistant(message, lang_code, context_text, api_key)

    # 2. Fallback if LLM unavailable or offline
    if not reply:
        reply = fallback_assistant_engine(message, lang_code, care_plan_context)

    return {
        "reply": reply,
        "language": lang_code,
        "language_name": LANGUAGE_NAMES.get(lang_code, "English"),
        "voice_lang_code": voice_code,
        "suggested_questions": SUGGESTED_QUESTIONS.get(lang_code, SUGGESTED_QUESTIONS["en"]),
        "safety_disclaimer": "CareBridge Voice Assistant communicates existing clinician orders. For clinical emergencies, call 108 or 112 immediately."
    }
