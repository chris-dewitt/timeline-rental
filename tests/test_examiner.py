"""Tests for examiner response fallbacks."""

from timeline_rental.narrative.ollama import generate_examiner_response


def test_examiner_response_fallback():
    result = generate_examiner_response(
        scene_context="question 1",
        player_choice="Yesterday. I was wrong.",
        question_index=0,
    )
    assert len(result["text"]) > 10
    assert result["source"] in ("ollama", "fallback")
