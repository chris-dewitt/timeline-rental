"""Curated narrative content — examiner, outcomes, déjà vu."""

from __future__ import annotations

OUTCOME_BUNDLES = [
    {
        "id": 0,
        "ending_title": "TIMELINE A — MERCY IN FRAME",
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
        "ending_title": "TIMELINE B — EDITED OUT",
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
        "ending_title": "TIMELINE C — WRONG SELF",
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

EXAMINER_QUESTIONS = [
    {
        "question": "Describe, in as much detail as you can, the last time you felt certain.",
        "choices": [
            ("1", "Yesterday. I was wrong.", 0),
            ("2", "I don't remember certainty.", 1),
        ],
        "fallback_response": "Certainty is a luxury. In this city, it's usually rented.",
    },
    {
        "question": "You see a wasp crawling on your arm. What do you do?",
        "choices": [
            ("1", "Let it walk. Count the steps.", 0),
            ("2", "Brush it off before it remembers me.", 1),
        ],
        "fallback_response": "Interesting. Most people lie about the wasp. You didn't. Or you lied differently.",
    },
    {
        "question": "A phone buzzes with a notification you already read. How do you feel?",
        "choices": [
            ("1", "Like time folded wrong.", 0),
            ("2", "Nothing. I feel nothing.", 1),
        ],
        "fallback_response": "The test isn't about the phone. It's about how many versions of you reached for it.",
    },
]

DEJA_VU_LINES = [
    "",
    "…you've been here. or someone like you.",
    "…three versions of this room still exist.",
    "…the photo hasn't decided yet.",
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
PHOTO_HINT = "the photo superposes. observe it [E] when you're ready."
SESSIONS_GRAFFITI = "you scrolled past your own funeral again"
