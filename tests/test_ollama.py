"""Tests for Ollama fallbacks (offline-safe)."""

from timeline_rental.narrative.ollama import (
    generate_clerk_fragment,
    generate_collapse_narration,
)


def test_collapse_narration_fallback():
    result = generate_collapse_narration(
        tape="blade runner [damaged]",
        photo_label="empty street",
        measured_bitstring="110",
        lost_timelines=["timeline A", "timeline C"],
        seed_narration="The street was always empty.",
    )
    assert result["text"]
    assert result["source"] in ("ollama", "fallback")


def test_clerk_fragment_fallback():
    result = generate_clerk_fragment(
        context="store hub",
        returns_count=0,
        last_receipt="",
    )
    assert len(result["text"]) > 10
    assert result["source"] in ("ollama", "fallback")
