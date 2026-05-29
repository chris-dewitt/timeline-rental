"""Curated narrative content — Week 1 fallbacks (Ollama arrives Week 2)."""

from __future__ import annotations

OUTCOME_BUNDLES = [
    {
        "id": 0,
        "photo_label": "a woman turning away — almost remembered",
        "narration": (
            "The photo developed backward. A woman you almost recognize "
            "looks past the lens, past you, toward a version of the street "
            "that never learned your name."
        ),
        "receipt_line": "collapsed: mercy held in frame (timeline A)",
        "lost": [
            "timeline B — the street stayed empty",
            "timeline C — your face smiled wrong",
        ],
    },
    {
        "id": 1,
        "photo_label": "an empty street — you were never there",
        "narration": (
            "The photo developed backward. The street was always empty. "
            "You were the thing that wasn't supposed to be in frame."
        ),
        "receipt_line": "collapsed: you were edited out (timeline B)",
        "lost": [
            "timeline A — she waited in the doorway",
            "timeline C — your reflection refused you",
        ],
    },
    {
        "id": 2,
        "photo_label": "your face — wrong angle, wrong smile",
        "narration": (
            "The photo developed backward. Your face, but borrowed. "
            "The smile arrived a half-second late, like it watched you decide it."
        ),
        "receipt_line": "collapsed: wrong self observed (timeline C)",
        "lost": [
            "timeline A — memory without a name",
            "timeline B — rain without a witness",
        ],
    },
]

EXAMINER_LINES = [
    "Describe, in as much detail as you can, the last time you felt certain.",
    "Certainty is a luxury. In this city, it's usually rented.",
]

CHOICE_LABELS = [
    ("1", "Yesterday. I was wrong.", 0),
    ("2", "I don't remember certainty.", 1),
]

INTRO_LINES = [
    "timeline rental presents",
    "blade runner [damaged]",
    "",
    "the rain never stops in three of the timelines.",
    "",
    "arrow keys — walk   E — interact",
]

ALLEY_HINT = "NEXUS REPAIR — walk right. find the doorway. press E."
ROOM_HINT = "the examiner waits. choose 1 or 2. then observe the photo [E]."
