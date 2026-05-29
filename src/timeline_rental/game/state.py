from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GameState:
    seed: int = 1337
    choice_history: list[int] = field(default_factory=list)
    timelines_active: int = 3
    outcome_index: int | None = None
    measured_bitstring: str | None = None
    narration: str = ""
    receipt_line: str = ""
    lost_timelines: list[str] = field(default_factory=list)
    photo_label: str = ""
    run_id: int | None = None
    flash_frames: int = 0
