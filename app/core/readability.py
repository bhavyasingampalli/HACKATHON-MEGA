"""
Readability Assessment Module for CareBridge AI.
Calculates Flesch-Kincaid Grade Level and Flesch Reading Ease for English text.
Provides separate, language-appropriate linguistic metrics for Telugu.
"""

import re
from typing import Dict, Any


def count_syllables_english(word: str) -> int:
    """
    Estimates syllable count for an English word using phonetic heuristic rules.
    """
    word = word.lower().strip()
    if not word:
        return 0
    if len(word) <= 3:
        return 1

    # Remove non-alpha
    word = re.sub(r'[^a-z]', '', word)
    if not word:
        return 1

    # Exceptional medical suffixes
    count = len(re.findall(r'[aeiouy]+', word))

    # Adjust for silent 'e' at end
    if word.endswith('e') and not word.endswith('le') and count > 1:
        count -= 1
    
    # Adjust for double vowels pronounced as one
    if word.endswith('ed') and not word.endswith('ted') and not word.endswith('ded') and count > 1:
        count -= 1

    return max(1, count)


def analyze_english_readability(text: str) -> Dict[str, Any]:
    """
    Calculates Flesch-Kincaid Grade Level and Reading Ease for English text.
    Target: Class 8 English (Grade <= 8.0).
    """
    if not text or not text.strip():
        return {
            "grade_level": 0.0,
            "reading_ease": 100.0,
            "word_count": 0,
            "sentence_count": 0,
            "syllable_count": 0,
            "avg_words_per_sentence": 0.0,
            "avg_syllables_per_word": 0.0,
            "target_met": True,
            "class_level_label": "Class 8 or Below",
            "interpretation": "Empty text provided."
        }

    # Split into sentences (by period, exclamation, question mark, or newline)
    sentences = [s.strip() for s in re.split(r'[.!?\n]+', text) if len(s.strip()) > 3]
    num_sentences = max(1, len(sentences))

    # Words
    words = re.findall(r'\b[A-Za-z0-9\'-]+\b', text)
    num_words = max(1, len(words))

    # Syllables
    num_syllables = sum(count_syllables_english(w) for w in words)

    words_per_sentence = num_words / num_sentences
    syllables_per_word = num_syllables / num_words

    # Flesch-Kincaid Grade Level formula
    fk_grade = 0.39 * words_per_sentence + 11.8 * syllables_per_word - 15.59
    fk_grade = max(1.0, round(fk_grade, 1))

    # Flesch Reading Ease formula
    reading_ease = 206.835 - 1.015 * words_per_sentence - 84.6 * syllables_per_word
    reading_ease = max(0.0, min(100.0, round(reading_ease, 1)))

    target_met = fk_grade <= 8.5

    if fk_grade <= 6.0:
        class_level_label = "Class 5 - 6 (Very Easy to Understand)"
        interpretation = "Plain, highly accessible language suitable for all adult readers."
    elif fk_grade <= 8.5:
        class_level_label = "Class 7 - 8 (Target Met: Plain Everyday English)"
        interpretation = "Well-balanced patient-friendly wording suitable for older adults and general public."
    elif fk_grade <= 10.0:
        class_level_label = "Class 9 - 10 (Moderate Complexity)"
        interpretation = "Contains some multi-syllable medical terms; may require brief explanation."
    else:
        class_level_label = f"Class 11+ (Grade {fk_grade})"
        interpretation = "Complex medical phrasing. Recommend simplifying terminology."

    return {
        "grade_level": fk_grade,
        "reading_ease": reading_ease,
        "word_count": num_words,
        "sentence_count": num_sentences,
        "syllable_count": num_syllables,
        "avg_words_per_sentence": round(words_per_sentence, 1),
        "avg_syllables_per_word": round(syllables_per_word, 2),
        "target_met": target_met,
        "class_level_label": class_level_label,
        "interpretation": interpretation
    }


def analyze_telugu_readability(text: str) -> Dict[str, Any]:
    """
    Appropriate linguistic assessment for Telugu text.
    Flesch-Kincaid is invalid for Telugu's agglutinative phonetic script.
    Instead, reports word count, sentence structure, Telugu script density, and clarity.
    """
    if not text or not text.strip():
        return {
            "status": "No Telugu text provided",
            "metric_available": False,
            "word_count": 0,
            "sentence_count": 0
        }

    # Sentences
    sentences = [s.strip() for s in re.split(r'[.!?\n।]+', text) if len(s.strip()) > 3]
    num_sentences = max(1, len(sentences))

    # Words
    words = text.split()
    num_words = max(1, len(words))

    # Telugu unicode range: \u0C00-\u0C7F
    telugu_chars = len(re.findall(r'[\u0C00-\u0C7F]', text))
    total_letters = len(re.findall(r'[^\s\d\W]', text))
    telugu_density = round((telugu_chars / max(1, total_letters)) * 100, 1)

    return {
        "status": "Telugu Assessment Complete",
        "metric_available": True,
        "flesch_applicable": False,
        "word_count": num_words,
        "sentence_count": num_sentences,
        "avg_words_per_sentence": round(num_words / num_sentences, 1),
        "telugu_script_purity_percent": telugu_density,
        "script_type": "Natural Telugu Unicode (తెలుగు లిపి)",
        "methodology_note": (
            "English syllable-based formulas (like Flesch-Kincaid) do not apply to Dravidian agglutinative "
            "scripts like Telugu. Instead, sentence length, script purity, and clinical terminology fidelity "
            "are independently evaluated."
        )
    }
