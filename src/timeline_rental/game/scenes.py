"""Scene implementations — alley, room, receipt."""

from __future__ import annotations

from timeline_rental.data.db import save_run
from timeline_rental.game.constants import INTERNAL_H, INTERNAL_W, TAPE_NAME
from timeline_rental.game.render import (
    Typewriter,
    draw_alley,
    draw_dialogue_box,
    draw_neon_sign,
    draw_player,
    draw_room,
    draw_timeline_hud,
)
from timeline_rental.game.state import GameState
from timeline_rental.narrative.content import (
    ALLEY_HINT,
    CHOICE_LABELS,
    EXAMINER_LINES,
    INTRO_LINES,
    OUTCOME_BUNDLES,
    ROOM_HINT,
)
from timeline_rental.quantum.collapse import collapse_timeline


class IntroScene:
    name = "intro"

    def __init__(self) -> None:
        self.writer = Typewriter(INTRO_LINES, chars_per_sec=22)

    def update(self, dt: float, state: GameState) -> str | None:
        self.writer.update(dt)
        if self.writer.done:
            return "alley"
        return None

    def handle_event(self, event, state: GameState) -> str | None:
        import pygame

        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.writer.skip()
            return "alley"
        return None

    def draw(self, canvas, mono, serif, rain, flicker: bool) -> None:
        draw_alley(canvas)
        rain.draw(canvas)
        lines = self.writer.visible_text()
        draw_dialogue_box(canvas, mono, serif, lines, y=60)


class AlleyScene:
    name = "alley"

    def __init__(self) -> None:
        self.player_x = 24
        self.player_y = 132
        self.show_hint = True
        self.writer = Typewriter([ALLEY_HINT], chars_per_sec=40)

    def update(self, dt: float, state: GameState) -> str | None:
        self.writer.update(dt)
        return None

    def handle_event(self, event, state: GameState) -> str | None:
        import pygame

        if event.type != pygame.KEYDOWN:
            return None
        if event.key == pygame.K_LEFT:
            self.player_x = max(8, self.player_x - 4)
        elif event.key == pygame.K_RIGHT:
            self.player_x = min(INTERNAL_W - 12, self.player_x + 4)
        elif event.key in (pygame.K_e, pygame.K_UP):
            if self.player_x > 250:
                return "room"
        return None

    def draw(self, canvas, mono, serif, rain, flicker: bool) -> None:
        draw_alley(canvas)
        draw_neon_sign(canvas, mono, "NEXUS REPAIR", flicker)
        # doorway glow
        pygame = __import__("pygame")
        pygame.draw.rect(canvas, (30, 40, 55), (270, 90, 30, 50))
        pygame.draw.rect(canvas, (0, 80, 90), (278, 110, 14, 28))
        draw_player(canvas, self.player_x, self.player_y)
        rain.draw(canvas)
        if self.show_hint:
            draw_dialogue_box(canvas, mono, serif, self.writer.visible_text(), y=148)


class RoomScene:
    name = "room"

    def __init__(self) -> None:
        self.phase = "question"  # question | chosen | observe
        self.writer = Typewriter([EXAMINER_LINES[0]], chars_per_sec=24)
        self.response_writer: Typewriter | None = None
        self.frame = 0

    def update(self, dt: float, state: GameState) -> str | None:
        self.frame += 1
        self.writer.update(dt)
        if self.response_writer:
            self.response_writer.update(dt)
        return None

    def _collapse(self, state: GameState) -> str:
        result = collapse_timeline(state.choice_history, state.seed)
        bundle = OUTCOME_BUNDLES[result.outcome_index]
        state.outcome_index = result.outcome_index
        state.measured_bitstring = result.measured_bitstring
        state.timelines_active = 1
        state.narration = bundle["narration"]
        state.receipt_line = bundle["receipt_line"]
        state.lost_timelines = bundle["lost"]
        state.photo_label = bundle["photo_label"]
        state.flash_frames = 3
        state.run_id = save_run(
            {
                "tape": TAPE_NAME,
                "choice_history": state.choice_history,
                "outcome_index": result.outcome_index,
                "measured_bitstring": result.measured_bitstring,
                "narration": bundle["narration"],
                "receipt_line": bundle["receipt_line"],
                "lost_timelines": bundle["lost"],
                "photo_label": bundle["photo_label"],
            }
        )
        return "receipt"

    def handle_event(self, event, state: GameState) -> str | None:
        import pygame

        if event.type != pygame.KEYDOWN:
            return None

        if self.phase == "question" and self.writer.done:
            for key, _label, choice_val in CHOICE_LABELS:
                if event.unicode == key or event.key == getattr(pygame, f"K_{key}"):
                    state.choice_history.append(choice_val)
                    self.phase = "chosen"
                    self.response_writer = Typewriter(
                        [EXAMINER_LINES[1], "", ROOM_HINT], chars_per_sec=26
                    )
                    return None

        if self.phase == "chosen" and self.response_writer and self.response_writer.done:
            if event.key in (pygame.K_e, pygame.K_RETURN, pygame.K_SPACE):
                return self._collapse(state)

        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if not self.writer.done:
                self.writer.skip()
            elif self.response_writer and not self.response_writer.done:
                self.response_writer.skip()
        return None

    def draw(self, canvas, mono, serif, rain, flicker: bool) -> None:
        glitch = (self.frame // 8) if self.phase != "observe" else 0
        draw_room(canvas, glitch)
        draw_timeline_hud(canvas, mono, 3 if self.phase != "chosen" else 2)
        rain.draw(canvas)

        lines: list[str] = []
        if self.phase == "question":
            lines = ['"' + self.writer.visible_text()[0] + '"'] if self.writer.visible_text() else []
            if self.writer.done:
                for key, label, _ in CHOICE_LABELS:
                    lines.append(f"[{key}] {label}")
        elif self.response_writer:
            lines = self.response_writer.visible_text()

        draw_dialogue_box(canvas, mono, serif, lines, y=108)


class ReceiptScene:
    name = "receipt"

    def __init__(self, state: GameState) -> None:
        lines = [
            "══════════════════════",
            " TIMELINE RENTAL — SLIP",
            "══════════════════════",
            f" TAPE: {TAPE_NAME}",
            f" {state.receipt_line}",
            "",
            f" PHOTO: {state.photo_label}",
            "",
            f" {state.narration[:44]}",
            f" {state.narration[44:88]}",
            "",
            " LOST:",
        ]
        for lost in state.lost_timelines:
            lines.append(f"  — {lost}")
        lines.extend(["", "R — rent again   Q — quit"])
        self.writer = Typewriter(lines, chars_per_sec=32)

    def update(self, dt: float, state: GameState) -> str | None:
        self.writer.update(dt)
        return None

    def handle_event(self, event, state: GameState) -> str | None:
        import pygame

        if event.type != pygame.KEYDOWN:
            return None
        if event.key == pygame.K_r:
            state.choice_history.clear()
            state.timelines_active = 3
            state.outcome_index = None
            state.flash_frames = 0
            return "intro"
        if event.key == pygame.K_q:
            return "quit"
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.writer.skip()
        return None

    def draw(self, canvas, mono, serif, rain, flicker: bool) -> None:
        canvas.fill((8, 8, 12))
        draw_dialogue_box(canvas, mono, serif, self.writer.visible_text(), y=20)
        rain.draw(canvas)
