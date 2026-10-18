"""
Tests for Readability Scoring (Flesch-Kincaid & Telugu linguistic assessment).
"""

import pytest
from app.core.readability import (
    analyze_english_readability,
    analyze_telugu_readability,
    count_syllables_english
)


def test_syllable_counter():
    assert count_syllables_english("take") == 1
    assert count_syllables_english("water") == 2
    assert count_syllables_english("medicine") >= 3
    assert count_syllables_english("tablet") == 2


def test_english_readability_class_8_target():
    # Simple plain language text
    simple_text = (
        "Take one tablet by mouth twice a day after food. "
        "Drink a full glass of water with each dose. "
        "Do not skip your meals. Call your doctor if you feel dizzy or have severe pain."
    )
    res = analyze_english_readability(simple_text)

    assert res["grade_level"] <= 8.5
    assert res["target_met"] is True
    assert res["word_count"] > 20
    assert res["sentence_count"] == 4


def test_telugu_linguistic_assessment():
    telugu_text = "రోజుకు రెండుసార్లు భోజనం తర్వాత ఒక మాత్ర నీటితో మింగాలి. పండ్ల రసాలు మరియు ఆకుకూరలు ఎక్కువగా తినండి."
    res = analyze_telugu_readability(telugu_text)

    assert res["metric_available"] is True
    assert res["flesch_applicable"] is False
    assert res["word_count"] > 5
    assert res["telugu_script_purity_percent"] > 80.0
