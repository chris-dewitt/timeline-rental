"""Local Ollama narration — sync for pygame, fallbacks when offline."""

from __future__ import annotations

import os
import re
from pathlib import Path

import httpx

PROMPTS_DIR = Path(__file__).resolve().parents[3] / "prompts"

CLERK_FALLBACKS = [
    "that tape's been rewinding since tuesday. or maybe tuesday never happened here.",
    "return policy: no refunds across timelines. store credit only.",
    "someone returned blade runner at 3:14am. it was still inside when we opened.",
    "the rain in slot 7 is louder than the rain outside. don't ask why.",
    "you've been here before. the store remembers. or a version of you does.",
    "damaged means the ending keeps changing. we stopped labeling which one is true.",
    "keep the receipt. the lost timelines don't show up on your bank statement.",
    "casablanca's still missing. vertigo's been rewinding itself since before you walked in.",
]


def _load_prompt(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


def _ollama_generate(prompt: str, timeout: float = 20.0) -> str | None:
    host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3.2")
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(
                f"{host}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
            )
            response.raise_for_status()
            raw = response.json().get("response", "").strip()
            return raw if raw else None
    except (httpx.HTTPError, OSError):
        return None


def _clean_line(text: str, max_len: int = 220) -> str:
    line = re.sub(r"\s+", " ", text).strip().strip('"').strip("'")
    if len(line) > max_len:
        line = line[: max_len - 1].rsplit(" ", 1)[0] + "…"
    return line


def generate_collapse_narration(
    *,
    tape: str,
    photo_label: str,
    measured_bitstring: str,
    lost_timelines: list[str],
    seed_narration: str,
) -> dict[str, str | bool]:
    prompt = _load_prompt("collapse.txt").format(
        tape=tape,
        photo_label=photo_label,
        measured_bitstring=measured_bitstring,
        lost_timelines="; ".join(lost_timelines),
        seed_narration=seed_narration,
    )
    raw = _ollama_generate(prompt)
    if raw:
        cleaned = _clean_line(raw, max_len=280)
        if len(cleaned) > 24:
            return {"text": cleaned, "generated": True, "source": "ollama"}

    return {"text": seed_narration, "generated": False, "source": "fallback"}


def generate_clerk_fragment(
    *,
    context: str,
    returns_count: int,
    last_receipt: str,
) -> dict[str, str | bool]:
    prompt = _load_prompt("clerk.txt").format(
        context=context,
        returns_count=returns_count,
        last_receipt=last_receipt or "none yet",
    )
    raw = _ollama_generate(prompt, timeout=15.0)
    if raw:
        cleaned = _clean_line(raw, max_len=120)
        if len(cleaned) > 12:
            return {"text": cleaned, "generated": True, "source": "ollama"}

    idx = (returns_count + len(last_receipt)) % len(CLERK_FALLBACKS)
    return {"text": CLERK_FALLBACKS[idx], "generated": False, "source": "fallback"}


EXAMINER_FALLBACKS = [
    "Certainty is a luxury. In this city, it's usually rented.",
    "Interesting. Most people lie about the wasp. You didn't.",
    "The test isn't about the phone. It's about how many versions of you reached for it.",
]


def generate_examiner_response(
    *,
    scene_context: str,
    player_choice: str,
    question_index: int,
    choice_value: int | None = None,
) -> dict[str, str | bool]:
    prompt = _load_prompt("examiner.txt").format(
        scene_context=scene_context,
        player_choice=player_choice,
    )
    raw = _ollama_generate(prompt, timeout=12.0)
    if raw:
        cleaned = _clean_line(raw, max_len=140)
        if len(cleaned) > 16:
            return {"text": cleaned, "generated": True, "source": "ollama"}

    from timeline_rental.narrative.content import EXAMINER_QUESTIONS

    if 0 <= question_index < len(EXAMINER_QUESTIONS):
        q = EXAMINER_QUESTIONS[question_index]
        by_choice = q.get("fallback_responses") or {}
        if choice_value is not None and choice_value in by_choice:
            return {"text": by_choice[choice_value], "generated": False, "source": "fallback"}
        if q.get("fallback_response"):
            return {"text": q["fallback_response"], "generated": False, "source": "fallback"}

    fb = EXAMINER_FALLBACKS[question_index % len(EXAMINER_FALLBACKS)]
    return {"text": fb, "generated": False, "source": "fallback"}
