"""Reset state between tape rentals."""

from __future__ import annotations

import random

from timeline_rental.game.state import GameState


def reset_run(state: GameState) -> None:
    state.seed = random.randint(0, 2**31 - 1)
    state.choice_history.clear()
    state.timelines_active = 3
    state.outcome_index = None
    state.measured_bitstring = None
    state.narration = ""
    state.receipt_line = ""
    state.lost_timelines.clear()
    state.photo_label = ""
    state.run_id = None
    state.flash_frames = 0
    state.narration_source = "fallback"
    state.clerk_source = "fallback"
    state.ending_title = ""
    state.photo_weights = (0.33, 0.33, 0.34)
    state.examiner_step = 0
