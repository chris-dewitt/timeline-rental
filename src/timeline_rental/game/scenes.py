"""Scene implementations — store hub, alley, room, receipt."""

from __future__ import annotations

from timeline_rental.data.db import get_run, list_runs, run_count, save_run
from timeline_rental.game.constants import INTERNAL_W, TAPE_NAME
from timeline_rental.game.render import (
    Typewriter,
    draw_alley,
    draw_dialogue_box,
    draw_neon_sign,
    draw_player,
    draw_room,
    draw_store,
    draw_timeline_hud,
    wrap_text,
)
from timeline_rental.game.run_reset import reset_run
from timeline_rental.game.state import GameState
from timeline_rental.narrative.content import (
    ALLEY_HINT,
    DEJA_VU_LINES,
    EXAMINER_QUESTIONS,
    INTRO_LINES,
    OUTCOME_BUNDLES,
    PHOTO_HINT,
    SESSIONS_GRAFFITI,
)
from timeline_rental.narrative.ollama import (
    generate_clerk_fragment,
    generate_collapse_narration,
    generate_examiner_response,
)
from timeline_rental.quantum.collapse import collapse_timeline
from timeline_rental.quantum.photo import photo_superposition


class StoreScene:
    name = "store"

    def __init__(self) -> None:
        self.frame = 0
        self.gallery_open = False
        self.gallery_index = 0
        self.gallery_detail: dict | None = None
        self.runs: list[dict] = []
        self.clerk_line = ""
        self.clerk_writer: Typewriter | None = None
        self._refresh_clerk()

    def _refresh_clerk(self) -> None:
        self.runs = list_runs(limit=20)
        last = self.runs[0]["receipt_line"] if self.runs else ""
        result = generate_clerk_fragment(
            context="player at timeline rental between tapes",
            returns_count=run_count(),
            last_receipt=last,
        )
        self.clerk_line = result["text"]
        self.clerk_writer = Typewriter([f'clerk: "{self.clerk_line}"'], chars_per_sec=28)

    def update(self, dt: float, state: GameState) -> str | None:
        self.frame += 1
        if self.clerk_writer and not self.gallery_open:
            self.clerk_writer.update(dt)
        return None

    def handle_event(self, event, state: GameState) -> str | None:
        import pygame

        if event.type != pygame.KEYDOWN:
            return None

        if self.gallery_detail:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE, pygame.K_g):
                self.gallery_detail = None
            return None

        if self.gallery_open:
            if event.key == pygame.K_ESCAPE:
                self.gallery_open = False
                return None
            if event.key == pygame.K_UP:
                self.gallery_index = max(0, self.gallery_index - 1)
            elif event.key == pygame.K_DOWN:
                self.gallery_index = min(len(self.runs) - 1, self.gallery_index + 1)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE) and self.runs:
                self.gallery_detail = get_run(self.runs[self.gallery_index]["id"])
            return None

        if event.key == pygame.K_g and self.runs:
            self.gallery_open = True
            self.gallery_index = 0
            return None
        if event.key == pygame.K_e:
            reset_run(state)
            return "intro"
        if event.key == pygame.K_q:
            return "quit"
        if event.key in (pygame.K_RETURN, pygame.K_SPACE) and self.clerk_writer:
            self.clerk_writer.skip()
        return None

    def draw(self, canvas, mono, serif, rain, flicker: bool) -> None:
        draw_store(canvas, mono, self.frame, flicker)
        rain.draw(canvas)

        if self.gallery_detail:
            self._draw_gallery_detail(canvas, mono, serif)
            return

        if self.gallery_open:
            self._draw_gallery_list(canvas, mono, serif)
            return

        lines = [
            "[E] insert blade runner [damaged]",
        ]
        if self.runs:
            lines.append(f"[G] receipt gallery ({len(self.runs)})")
        lines.append("[Q] quit")
        if self.clerk_writer:
            lines = self.clerk_writer.visible_text() + [""] + lines
        draw_dialogue_box(canvas, mono, serif, lines, y=118)

    def _draw_gallery_list(self, canvas, mono, serif) -> None:
        lines = ["—— receipt gallery ——"]
        for i, run in enumerate(self.runs[:6]):
            prefix = ">" if i == self.gallery_index else " "
            lines.append(f"{prefix} #{run['id']} {run['receipt_line'][:34]}")
        lines.extend(["", "up/down — browse   enter — read", "esc — back"])
        draw_dialogue_box(canvas, mono, serif, lines, y=14)

    def _draw_gallery_detail(self, canvas, mono, serif) -> None:
        assert self.gallery_detail
        run = self.gallery_detail
        lines = [
            f"RETURN SLIP #{run['id']}",
            run["receipt_line"],
            f"photo: {run['photo_label']}",
            f"|ψ⟩ → {run['measured_bitstring']}",
            "",
        ]
        lines.extend(wrap_text(run["narration"], 38)[:3])
        lines.append("")
        lines.append("LOST:")
        for lost in run["lost_timelines"][:2]:
            lines.append(f" — {lost}")
        if run.get("clerk_fragment"):
            lines.extend(["", f"clerk: {run['clerk_fragment'][:40]}"])
        lines.extend(["", "esc — back"])
        draw_dialogue_box(canvas, mono, serif, lines, y=8)


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
        draw_timeline_hud(canvas, mono, 3)
        draw_dialogue_box(canvas, mono, serif, self.writer.visible_text(), y=60)


class AlleyScene:
    name = "alley"

    def __init__(self) -> None:
        self.player_x = 24
        self.player_y = 132
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
        import pygame

        draw_alley(canvas, SESSIONS_GRAFFITI)
        draw_neon_sign(canvas, mono, "NEXUS REPAIR", flicker)
        draw_timeline_hud(canvas, mono, 3)
        pygame.draw.rect(canvas, (30, 40, 55), (270, 90, 30, 50))
        pygame.draw.rect(canvas, (0, 80, 90), (278, 110, 14, 28))
        draw_player(canvas, self.player_x, self.player_y)
        rain.draw(canvas)
        draw_dialogue_box(canvas, mono, serif, self.writer.visible_text(), y=148)


class RoomScene:
    name = "room"

    def __init__(self) -> None:
        self.phase = "question"
        self.question_index = 0
        self.writer: Typewriter | None = None
        self.response_writer: Typewriter | None = None
        self.develop_writer: Typewriter | None = None
        self.frame = 0
        self.pending_collapse = False
        self.collapse_delay = 0.0
        self.initialized = False
        self._last_weights = (0.33, 0.33, 0.34)
        self._start_question()

    def _start_question(self) -> None:
        q = EXAMINER_QUESTIONS[self.question_index]
        self.writer = Typewriter([q["question"]], chars_per_sec=24)
        self.response_writer = None
        self.phase = "question"

    def _ensure_photo_state(self, state: GameState) -> None:
        if not self.initialized:
            sup = photo_superposition(state.seed)
            state.photo_weights = sup.weights
            self._last_weights = sup.weights
            state.timelines_active = 3
            self.initialized = True

    def update(self, dt: float, state: GameState) -> str | None:
        self.frame += 1
        self._ensure_photo_state(state)
        if self.writer:
            self.writer.update(dt)
        if self.response_writer:
            self.response_writer.update(dt)
        if self.develop_writer:
            self.develop_writer.update(dt)

        if self.pending_collapse:
            self.collapse_delay -= dt
            if self.collapse_delay <= 0:
                self.pending_collapse = False
                return self._collapse(state)
        return None

    def _collapse(self, state: GameState) -> str:
        result = collapse_timeline(state.choice_history, state.seed)
        bundle = OUTCOME_BUNDLES[result.outcome_index]

        narration = generate_collapse_narration(
            tape=TAPE_NAME,
            photo_label=bundle["photo_label"],
            measured_bitstring=result.measured_bitstring,
            lost_timelines=bundle["lost"],
            seed_narration=bundle["narration"],
        )
        clerk = generate_clerk_fragment(
            context="player just returned a collapsed blade runner tape",
            returns_count=run_count() + 1,
            last_receipt=bundle["receipt_line"],
        )

        state.outcome_index = result.outcome_index
        state.measured_bitstring = result.measured_bitstring
        state.timelines_active = 1
        state.narration = str(narration["text"])
        state.narration_source = str(narration["source"])
        state.receipt_line = bundle["receipt_line"]
        state.ending_title = bundle["ending_title"]
        state.lost_timelines = bundle["lost"]
        state.photo_label = bundle["photo_label"]
        state.clerk_fragment = str(clerk["text"])
        state.clerk_source = str(clerk["source"])
        state.flash_frames = 3

        state.run_id = save_run(
            {
                "tape": TAPE_NAME,
                "choice_history": state.choice_history,
                "outcome_index": result.outcome_index,
                "measured_bitstring": result.measured_bitstring,
                "narration": state.narration,
                "receipt_line": bundle["receipt_line"],
                "ending_title": bundle["ending_title"],
                "lost_timelines": bundle["lost"],
                "photo_label": bundle["photo_label"],
                "clerk_fragment": state.clerk_fragment,
            }
        )
        return "receipt"

    def _advance_after_response(self, state: GameState) -> None:
        self.question_index += 1
        state.examiner_step = self.question_index
        if self.question_index >= len(EXAMINER_QUESTIONS):
            self.phase = "photo"
            self.writer = Typewriter([PHOTO_HINT], chars_per_sec=26)
        else:
            self._start_question()

    def handle_event(self, event, state: GameState) -> str | None:
        import pygame

        if event.type != pygame.KEYDOWN:
            return None

        if self.phase == "developing":
            return None

        if self.phase == "question" and self.writer and self.writer.done:
            q = EXAMINER_QUESTIONS[self.question_index]
            for key, label, choice_val in q["choices"]:
                if event.unicode == key or event.key == getattr(pygame, f"K_{key}"):
                    state.choice_history.append(choice_val)
                    resp = generate_examiner_response(
                        scene_context=f"voight-kampff question {self.question_index + 1} of 3",
                        player_choice=label,
                        question_index=self.question_index,
                    )
                    lines = [f'"{resp["text"]}"']
                    if self.question_index + 1 < len(DEJA_VU_LINES):
                        deja = DEJA_VU_LINES[self.question_index + 1]
                        if deja:
                            lines.append(deja)
                    self.phase = "response"
                    self.response_writer = Typewriter(lines, chars_per_sec=26)
                    return None

        if self.phase == "response" and self.response_writer and self.response_writer.done:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._advance_after_response(state)
                return None

        if self.phase == "photo" and self.writer and self.writer.done:
            if event.key in (pygame.K_e, pygame.K_RETURN, pygame.K_SPACE):
                self.phase = "developing"
                self.develop_writer = Typewriter(
                    [
                        "the photo develops...",
                        "three versions fight for the frame...",
                        "listening for which timeline survives...",
                    ],
                    chars_per_sec=18,
                )
                self.pending_collapse = True
                self.collapse_delay = 1.0
                return None

        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if self.writer and not self.writer.done:
                self.writer.skip()
            elif self.response_writer and not self.response_writer.done:
                self.response_writer.skip()
        return None

    def draw(self, canvas, mono, serif, rain, flicker: bool) -> None:
        weights = getattr(self, "_last_weights", (0.33, 0.33, 0.34))
        photo_phase = self.phase in {"photo", "developing"}
        draw_room(canvas, self.frame, weights, photo_phase=photo_phase)
        draw_timeline_hud(canvas, mono, 1 if self.phase == "developing" else 3)
        rain.draw(canvas)

        lines: list[str] = []
        if self.phase == "developing" and self.develop_writer:
            lines = self.develop_writer.visible_text()
        elif self.phase == "photo" and self.writer:
            lines = list(self.writer.visible_text())
            if self.writer.done:
                lines.append("[E] observe the photo")
        elif self.phase == "question" and self.writer:
            if self.writer.visible_text():
                lines = ['"' + self.writer.visible_text()[0] + '"']
            if self.writer.done:
                q = EXAMINER_QUESTIONS[self.question_index]
                for key, label, _ in q["choices"]:
                    lines.append(f"[{key}] {label}")
        elif self.phase == "response" and self.response_writer:
            visible = self.response_writer.visible_text()
            lines = list(visible)
            if self.response_writer.done:
                lines.append("[space] continue")

        draw_dialogue_box(canvas, mono, serif, lines, y=100, max_lines=6)


class ReceiptScene:
    name = "receipt"

    def __init__(self, state: GameState) -> None:
        lines = [
            "══════════════════════",
            " TIMELINE RENTAL — SLIP",
            "══════════════════════",
            f" {state.ending_title or 'COLLAPSED TIMELINE'}",
            f" TAPE: {TAPE_NAME}",
            f" {state.receipt_line}",
            f" |ψ⟩ → {state.measured_bitstring}",
            "",
            f" PHOTO: {state.photo_label}",
            "",
        ]
        lines.extend(wrap_text(state.narration, 38)[:4])
        lines.extend(["", " LOST:"])
        for lost in state.lost_timelines:
            lines.append(f"  — {lost}")
        if state.clerk_fragment:
            lines.extend(["", f" clerk: {state.clerk_fragment[:42]}"])
        src = "ollama" if state.narration_source == "ollama" else "curated"
        lines.extend(["", f" ({src} narration)", "", "ENTER — return to store"])
        lines.extend([" R — rent again   Q — quit"])
        self.writer = Typewriter(lines, chars_per_sec=30)

    def update(self, dt: float, state: GameState) -> str | None:
        self.writer.update(dt)
        return None

    def handle_event(self, event, state: GameState) -> str | None:
        import pygame

        if event.type != pygame.KEYDOWN:
            return None
        if event.key == pygame.K_r:
            reset_run(state)
            return "intro"
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if not self.writer.done:
                self.writer.skip()
            else:
                return "store"
        if event.key == pygame.K_q:
            return "quit"
        return None

    def draw(self, canvas, mono, serif, rain, flicker: bool) -> None:
        canvas.fill((8, 8, 12))
        draw_dialogue_box(canvas, mono, serif, self.writer.visible_text(), y=8, max_lines=10)
        rain.draw(canvas)
