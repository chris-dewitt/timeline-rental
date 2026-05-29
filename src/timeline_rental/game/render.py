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
    surface.blit(label, (8, 6))


def draw_dialogue_box(
    surface: pygame.Surface,
    mono: pygame.font.Font,
    serif: pygame.font.Font,
    lines: list[str],
    *,
    y: int = 118,
) -> None:
    pygame.draw.rect(surface, (18, 18, 26), (6, y, INTERNAL_W - 12, INTERNAL_H - y - 6))
    pygame.draw.rect(surface, SMOG_GRAY, (6, y, INTERNAL_W - 12, INTERNAL_H - y - 6), 1)
    for i, line in enumerate(lines[:4]):
        font = serif if line.startswith('"') or len(line) > 28 else mono
        color = REPLICANT_AMBER if line.startswith("[") else WET_WHITE
        rendered = font.render(line[:46], True, color)
        surface.blit(rendered, (12, y + 6 + i * 11))


def draw_player(surface: pygame.Surface, x: int, y: int) -> None:
    pygame.draw.rect(surface, NEON_CYAN, (x, y, 6, 10))
    pygame.draw.rect(surface, WET_WHITE, (x + 1, y + 2, 4, 3))


def draw_alley(surface: pygame.Surface) -> None:
    pygame.draw.rect(surface, RAIN_BLACK, (0, 0, INTERNAL_W, INTERNAL_H))
    # buildings
    pygame.draw.rect(surface, (18, 18, 28), (0, 40, 120, 140))
    pygame.draw.rect(surface, (22, 22, 34), (140, 55, 180, 125))
    # puddles
    for px in (40, 120, 210, 280):
        pygame.draw.ellipse(surface, PUDDLE, (px, 150, 24, 6))


def draw_room(surface: pygame.Surface, photo_glitch: int) -> None:
    pygame.draw.rect(surface, (10, 10, 16), (0, 0, INTERNAL_W, INTERNAL_H))
    pygame.draw.rect(surface, (28, 24, 22), (40, 70, 240, 50))  # table
    # photo
    ox = photo_glitch % 3 - 1
    pygame.draw.rect(surface, REPLICANT_AMBER, (148 + ox, 78, 24, 18))
    pygame.draw.rect(surface, (40, 30, 20), (150 + ox, 80, 20, 14))
    # examiner silhouette
    pygame.draw.rect(surface, SMOG_GRAY, (220, 52, 14, 28))
    pygame.draw.circle(surface, (255, 120, 40), (233, 58), 2)  # cigarette


def draw_collapse_flash(surface: pygame.Surface, strength: float) -> None:
    overlay = pygame.Surface((INTERNAL_W, INTERNAL_H), pygame.SRCALPHA)
    alpha = int(220 * strength)
    overlay.fill((255, 154, 60, alpha))
    surface.blit(overlay, (0, 0))
