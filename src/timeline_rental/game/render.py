"""Drawing helpers — rain, typewriter text, neon noir."""

from __future__ import annotations

import random

import pygame

from timeline_rental.game.constants import (
    INTERNAL_H,
    INTERNAL_W,
    NEON_CYAN,
    NEON_DIM,
    PUDDLE,
    RAIN_BLACK,
    REPLICANT_AMBER,
    SMOG_GRAY,
    WET_WHITE,
)


class Rain:
    def __init__(self, count: int = 90) -> None:
        self.drops = [
            {
                "x": random.randint(0, INTERNAL_W),
                "y": random.randint(-INTERNAL_H, INTERNAL_H),
                "speed": random.uniform(2.5, 5.5),
            }
            for _ in range(count)
        ]

    def update(self) -> None:
        for drop in self.drops:
            drop["y"] += drop["speed"]
            if drop["y"] > INTERNAL_H:
                drop["y"] = random.randint(-20, -2)
                drop["x"] = random.randint(0, INTERNAL_W)

    def draw(self, surface: pygame.Surface) -> None:
        for drop in self.drops:
            pygame.draw.line(
                surface,
                (80, 100, 120),
                (int(drop["x"]), int(drop["y"])),
                (int(drop["x"] - 1), int(drop["y"] + 4)),
                1,
            )


class Typewriter:
    def __init__(self, lines: list[str], chars_per_sec: float = 28) -> None:
        self.lines = lines
        self.chars_per_sec = chars_per_sec
        self.elapsed = 0.0
        self.done = False

    def update(self, dt: float) -> None:
        if self.done:
            return
        self.elapsed += dt
        total_chars = sum(len(line) + 1 for line in self.lines)
        if self.elapsed * self.chars_per_sec >= total_chars:
            self.done = True

    def skip(self) -> None:
        self.done = True

    def visible_text(self) -> list[str]:
        if self.done:
            return self.lines
        budget = int(self.elapsed * self.chars_per_sec)
        visible: list[str] = []
        for line in self.lines:
            if budget <= 0:
                break
            if budget >= len(line):
                visible.append(line)
                budget -= len(line) + 1
            else:
                visible.append(line[:budget])
                budget = 0
        return visible


def load_fonts() -> tuple[pygame.font.Font, pygame.font.Font]:
    mono = pygame.font.SysFont("consolas,courier,monospace", 8)
    serif = pygame.font.SysFont("georgia,times,serif", 9)
    return mono, serif


def draw_scanlines(surface: pygame.Surface, alpha: int = 18) -> None:
    overlay = pygame.Surface((INTERNAL_W, INTERNAL_H), pygame.SRCALPHA)
    for y in range(0, INTERNAL_H, 3):
        pygame.draw.line(overlay, (0, 229, 255, alpha), (0, y), (INTERNAL_W, y), 1)
    surface.blit(overlay, (0, 0))


def draw_neon_sign(surface: pygame.Surface, font: pygame.font.Font, text: str, flicker: bool) -> None:
    color = NEON_CYAN if flicker else NEON_DIM
    label = font.render(text, True, color)
    x = INTERNAL_W // 2 - label.get_width() // 2
    pygame.draw.rect(surface, PUDDLE, (x - 4, 18, label.get_width() + 8, 12))
    surface.blit(label, (x, 20))


def draw_timeline_hud(surface: pygame.Surface, font: pygame.font.Font, active: int) -> None:
    label = font.render(f"TIMELINES: {active} active", True, NEON_CYAN)
    surface.blit(label, (INTERNAL_W - label.get_width() - 8, 6))


def draw_dialogue_box(
    surface: pygame.Surface,
    mono: pygame.font.Font,
    serif: pygame.font.Font,
    lines: list[str],
    *,
    y: int = 118,
    max_lines: int = 6,
) -> None:
    box_h = min(INTERNAL_H - y - 6, 8 + max_lines * 11)
    pygame.draw.rect(surface, (18, 18, 26), (6, y, INTERNAL_W - 12, box_h))
    pygame.draw.rect(surface, SMOG_GRAY, (6, y, INTERNAL_W - 12, box_h), 1)
    for i, line in enumerate(lines[:max_lines]):
        font = serif if line.startswith('"') or line.startswith("…") or len(line) > 28 else mono
        color = REPLICANT_AMBER if line.startswith("[") else WET_WHITE
        if line.startswith("…"):
            color = (140, 160, 180)
        rendered = font.render(line[:46], True, color)
        surface.blit(rendered, (12, y + 6 + i * 11))


def draw_player(surface: pygame.Surface, x: int, y: int) -> None:
    pygame.draw.rect(surface, NEON_CYAN, (x, y, 6, 10))
    pygame.draw.rect(surface, WET_WHITE, (x + 1, y + 2, 4, 3))


def draw_alley(surface: pygame.Surface, graffiti: str = "") -> None:
    pygame.draw.rect(surface, RAIN_BLACK, (0, 0, INTERNAL_W, INTERNAL_H))
    pygame.draw.rect(surface, (18, 18, 28), (0, 40, 120, 140))
    pygame.draw.rect(surface, (22, 22, 34), (140, 55, 180, 125))
    for px in (40, 120, 210, 280):
        pygame.draw.ellipse(surface, PUDDLE, (px, 150, 24, 6))
    if graffiti:
        font = pygame.font.SysFont("consolas,courier,monospace", 6)
        tag = font.render(graffiti[:28], True, (255, 42, 109))
        surface.blit(tag, (48, 118))


def _draw_photo_variant(surface: pygame.Surface, x: int, y: int, variant: int, alpha: int = 255) -> None:
    frame = pygame.Surface((20, 14), pygame.SRCALPHA)
    base = (40, 30, 20, alpha)
    accent = (REPLICANT_AMBER[0], REPLICANT_AMBER[1], REPLICANT_AMBER[2], alpha)
    highlight = (WET_WHITE[0], WET_WHITE[1], WET_WHITE[2], min(255, alpha + 40))

    if variant == 0:
        pygame.draw.circle(frame, accent, (14, 5), 3)
        pygame.draw.line(frame, highlight, (14, 8), (10, 13), 1)
        pygame.draw.line(frame, highlight, (14, 8), (18, 13), 1)
    elif variant == 1:
        pygame.draw.line(frame, (60, 70, 80, alpha), (2, 10), (18, 10), 1)
        pygame.draw.rect(frame, base, (4, 4, 12, 8))
    else:
        pygame.draw.rect(frame, base, (4, 3, 12, 10))
        pygame.draw.line(frame, (200, 80, 80, alpha), (7, 7), (7, 7), 1)
        pygame.draw.line(frame, (200, 80, 80, alpha), (13, 7), (13, 7), 1)
        pygame.draw.line(frame, accent, (6, 11), (15, 10), 1)

    surface.blit(frame, (x, y))


def draw_room(
    surface: pygame.Surface,
    frame: int,
    photo_weights: tuple[float, float, float],
    *,
    photo_phase: bool = False,
    collapsed_variant: int | None = None,
) -> None:
    pygame.draw.rect(surface, (10, 10, 16), (0, 0, INTERNAL_W, INTERNAL_H))
    pygame.draw.rect(surface, (28, 24, 22), (40, 70, 240, 50))
    pygame.draw.rect(surface, REPLICANT_AMBER, (148, 78, 24, 18))
    pygame.draw.rect(surface, (40, 30, 20), (150, 80, 20, 14))

    ox = frame % 3 - 1
    if collapsed_variant is not None:
        _draw_photo_variant(surface, 150 + ox, 80, collapsed_variant)
    elif photo_phase:
        from timeline_rental.quantum.photo import glitch_variant

        primary = glitch_variant(frame, photo_weights)
        secondary = (primary + 1) % 3
        blink = frame % 14 < 7
        _draw_photo_variant(surface, 150 + (0 if blink else 1), 80, primary, 255 if blink else 200)
        _draw_photo_variant(surface, 150 + (1 if blink else 0), 79, secondary, 90)
    else:
        v = (frame // 6) % 3
        _draw_photo_variant(surface, 150 + ox, 80, v, 160)

    pygame.draw.rect(surface, SMOG_GRAY, (220, 52, 14, 28))
    pygame.draw.circle(surface, (255, 120, 40), (233, 58), 2)
    pygame.draw.rect(surface, (35, 30, 28), (60, 82, 8, 10))


def draw_collapse_flash(surface: pygame.Surface, strength: float) -> None:
    overlay = pygame.Surface((INTERNAL_W, INTERNAL_H), pygame.SRCALPHA)
    alpha = int(220 * strength)
    overlay.fill((255, 154, 60, alpha))
    surface.blit(overlay, (0, 0))


def draw_store(surface: pygame.Surface, mono: pygame.font.Font, frame: int, flicker: bool) -> None:
    surface.fill((9, 9, 14))
    # shelves
    for sx in (8, 88, 168, 248):
        pygame.draw.rect(surface, (20, 20, 30), (sx, 36, 56, 100))
        pygame.draw.rect(surface, SMOG_GRAY, (sx, 36, 56, 100), 1)
    # CRT static
    static_color = WET_WHITE if frame % 5 < 2 else SMOG_GRAY
    pygame.draw.rect(surface, (14, 14, 20), (108, 52, 104, 58))
    pygame.draw.rect(surface, static_color, (112, 56, 96, 50), 1)
    for _ in range(18):
        px = 112 + (_ * 17 + frame * 3) % 96
        py = 58 + (_ * 11 + frame * 5) % 46
        pygame.draw.line(surface, (40, 50, 60), (px, py), (px + 4, py), 1)
    # glowing tape
    glow = NEON_CYAN if flicker else REPLICANT_AMBER
    pygame.draw.rect(surface, (18, 18, 28), (12, 48, 48, 14))
    pygame.draw.rect(surface, glow, (12, 48, 48, 14), 1)
    tape_label = mono.render("BLADE RUNNER", True, glow)
    surface.blit(tape_label, (14, 50))
    dmg = mono.render("[damaged]", True, REPLICANT_AMBER)
    surface.blit(dmg, (14, 58))
    # locked tapes
    for i, name in enumerate(("CASABLANCA", "VERTIGO")):
        y = 68 + i * 18
        label = mono.render(name, True, SMOG_GRAY)
        surface.blit(label, (178, y))
        lock = mono.render("[missing]", True, (50, 55, 65))
        surface.blit(lock, (178, y + 8))
    # sign
    sign = mono.render("TIMELINE RENTAL", True, NEON_CYAN if flicker else NEON_DIM)
    surface.blit(sign, (INTERNAL_W // 2 - sign.get_width() // 2, 8))
    open_label = mono.render("OPEN 24h (maybe)", True, SMOG_GRAY)
    surface.blit(open_label, (INTERNAL_W // 2 - open_label.get_width() // 2, 18))


def wrap_text(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines
