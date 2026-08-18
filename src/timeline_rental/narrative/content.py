"""Curated narrative content — examiner, outcomes, déjà vu."""

from __future__ import annotations

OUTCOME_BUNDLES = [
    {
        "id": 0,
        "ending_title": "TIMELINE A — MERCY IN FRAME",
        "photo_label": "a woman turning away — almost remembered",
        "narration": (
            "The emulsion chose mercy. A woman turns from the lens, coat collar up, "
            "as if she already knew which of you would survive the observation. "
            "Rain beads on her shoulder like punctuation. You almost say her name — "
            "then remember you never learned it in this timeline."
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
            "The photo developed backward into absence. Wet asphalt. Neon bleeding into a puddle. "
            "No figure in the doorway — not you, not anyone. "
            "You were the thing that wasn't supposed to be in frame, and the frame finally won."
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
            "The photo developed into a face that wears your bones like a costume. "
            "The smile arrives a half-second late, as if it watched you decide it. "
            "Somewhere behind the glass, three versions of you argue about who blinked first."
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
        "question": "Describe the last time you felt certain — not hopeful. Certain.",
        "choices": [
            ("1", "Yesterday. I was wrong.", 0),
            ("2", "I don't remember certainty.", 1),
        ],
        "fallback_responses": {
            0: "Honesty, or rehearsal. Under neon they look the same.",
            1: "Certainty is a luxury. Here, it's rented by the hour.",
        },
        "fallback_response": "Certainty is a luxury. In this city, it's usually rented.",
    },
    {
        "question": "A wasp lands on your wrist and walks toward your pulse. What do you do?",
        "choices": [
            ("1", "Let it walk. Count the steps.", 0),
            ("2", "Brush it off before it remembers me.", 1),
        ],
        "fallback_responses": {
            0: "Patience reads as empathy. Or as something waiting to strike.",
            1: "Most people lie about the wasp. You didn't. Or you lied differently.",
        },
        "fallback_response": (
            "Interesting. Most people lie about the wasp. You didn't. Or you lied differently."
        ),
    },
    {
        "question": "Your phone buzzes with a notification you already read. How does your chest answer?",
        "choices": [
            ("1", "Like time folded wrong.", 0),
            ("2", "Nothing. I feel nothing.", 1),
        ],
        "fallback_responses": {
            0: "Déjà vu is cheap. Choosing which memory keeps the receipt isn't.",
            1: "The test isn't the phone. It's how many of you reached for it.",
        },
        "fallback_response": (
            "The test isn't about the phone. It's about how many versions of you reached for it."
        ),
    },
]

DEJA_VU_LINES = [
    "",
    "…you've been here. or someone like you.",
    "…three versions of this room still exist. the rain knows which.",
    "…the photo hasn't decided which of you gets to be real.",
]

INTRO_LINES = [
    "timeline rental presents",
    "blade runner [damaged]",
    "",
    "a tape that keeps forgetting which ending it had.",
    "the rain never stops in three of the timelines.",
    "you are the observation event.",
    "",
    "arrow keys — walk   E — interact",
]

ALLEY_HINT = "walk right → doorway → press E"

ALLEY_BEATS = [
    (0, 80, "acid rain stitches neon into the street."),
    (80, 160, "puddles hold a second city — almost honest."),
    (160, 250, "a cigarette glows. someone is waiting. or was."),
    (250, 999, "NEXUS REPAIR flickers between open and never."),
]

ROOM_ENTER_LINES = [
    "the door seals rain out and doubt in.",
    "a table. a photo that won't stay still.",
    'examiner: "sit. we already started."',
]

PHOTO_HINT = "three histories fight for one emulsion."
PHOTO_HINT_PROMPT = "[E] observe — lose two timelines"

PHOTO_DEVELOP_LINES = [
    "the photo develops in wrong light...",
    "three versions claw for the frame...",
    "listening for which timeline survives the observation...",
]

SESSIONS_GRAFFITI = "scrolled past your own funeral"

STORE_TAGLINE = "OPEN 24h (maybe) — returns accepted across realities"
