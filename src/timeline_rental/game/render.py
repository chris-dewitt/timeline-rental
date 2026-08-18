"""Drawing helpers — rain, typewriter text, neon noir atmosphere."""

from __future__ import annotations

import random

import pygame

from timeline_rental.game.constants import (
    BLOOD_NEON,
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
    def __init__(self, count: int = 110) -> None:
        self.drops = [self._spawn(random.randint(-INTERNAL_H, INTERNAL_H)) for _ in range(count)]
        self.splashes: list[dict] = []

    def _spawn(self, y: int | None = None) -> dict:
        return {
            "x": random.uniform(0, INTERNAL_W),
            "y": float(y if y is not None else random.randint(-40, -2)),
            "speed": random.uniform(2.8, 6.2),
            "len": random.randint(3, 7),
            "alpha": random.randint(70, 160),
        }

    def update(self) -> None:
        street_y = 148
        for drop in self.drops:
            drop["y"] += drop["speed"]
            if drop["y"] > street_y:
                if random.random() < 0.35:
                    self.splashes.append(
                        {
                            "x": drop["x"],
                            "y": street_y + random.randint(0, 8),
                            "life": 4,
                        }
                    )
                drop.update(self._spawn())
        self.splashes = [s for s in self.splashes if s["life"] > 0]
        for splash in self.splashes:
            splash["life"] -= 1

    def draw(self, surface: pygame.Surface) -> None:
        for drop in self.drops:
            a = drop["alpha"]
            color = (90, 115, 140, a)
            tip = (int(drop["x"]), int(drop["y"]))
            line = pygame.Surface((3, drop["len"] + 2), pygame.SRCALPHA)
            pygame.draw.line(line, color, (2, 0), (0, drop["len"]), 1)
            surface.blit(line, (tip[0] - 1, tip[1]))
        for splash in self.splashes:
            a = 40 + splash["life"] * 30
            dot = pygame.Surface((4, 3), pygame.SRCALPHA)
            pygame.draw.circle(dot, (100, 120, 140, min(180, a)), (2, 1), 1)
            surface.blit(dot, (int(splash["x"]) - 2, int(splash["y"]) - 1))


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


def draw_scanlines(surface: pygame.Surface, alpha: int = 22) -> None:
    overlay = pygame.Surface((INTERNAL_W, INTERNAL_H), pygame.SRCALPHA)
    for y in range(0, INTERNAL_H, 2):
        a = alpha if y % 4 == 0 else max(8, alpha // 2)
        pygame.draw.line(overlay, (0, 0, 0, a), (0, y), (INTERNAL_W, y), 1)
    surface.blit(overlay, (0, 0))


def draw_vignette(surface: pygame.Surface, strength: int = 90) -> None:
    overlay = pygame.Surface((INTERNAL_W, INTERNAL_H), pygame.SRCALPHA)
    for i in range(28):
        a = int(strength * (i / 28) ** 1.6)
        pygame.draw.rect(overlay, (0, 0, 0, a), (i, i, INTERNAL_W - i * 2, INTERNAL_H - i * 2), 1)
    surface.blit(overlay, (0, 0))


def draw_neon_glow(
    surface: pygame.Surface,
    rect: tuple[int, int, int, int],
    color: tuple[int, int, int],
    *,
    layers: int = 3,
) -> None:
    x, y, w, h = rect
    for i in range(layers, 0, -1):
        a = 18 + i * 14
        pad = i * 2
        glow = pygame.Surface((w + pad * 2, h + pad * 2), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*color, a), (0, 0, w + pad * 2, h + pad * 2), border_radius=2)
        surface.blit(glow, (x - pad, y - pad))


def draw_neon_sign(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    flicker: bool,
    *,
    y: int = 20,
) -> None:
    color = NEON_CYAN if flicker else NEON_DIM
    label = font.render(text, True, color)
    x = INTERNAL_W // 2 - label.get_width() // 2
    draw_neon_glow(surface, (x - 4, y - 2, label.get_width() + 8, 12), color, layers=2)
    pygame.draw.rect(surface, (12, 18, 28), (x - 4, y - 2, label.get_width() + 8, 12))
    surface.blit(label, (x, y))
    # puddle reflection
    refl = font.render(text, True, (*color[:3],))
    refl = pygame.transform.flip(refl, False, True)
    refl.set_alpha(55 if flicker else 25)
    surface.blit(refl, (x, 152))


def draw_timeline_hud(surface: pygame.Surface, font: pygame.font.Font, active: int) -> None:
    text = f"TIMELINES: {active} active"
    label = font.render(text, True, NEON_CYAN if active > 1 else REPLICANT_AMBER)
    pad = 3
    box = pygame.Surface((label.get_width() + pad * 2, label.get_height() + pad * 2), pygame.SRCALPHA)
    pygame.draw.rect(box, (8, 12, 18, 180), box.get_rect())
    pygame.draw.rect(box, (*NEON_CYAN, 80), box.get_rect(), 1)
    box.blit(label, (pad, pad))
    surface.blit(box, (INTERNAL_W - box.get_width() - 6, 4))


def draw_dialogue_box(
    surface: pygame.Surface,
    mono: pygame.font.Font,
    serif: pygame.font.Font,
    lines: list[str],
    *,
    y: int = 118,
    max_lines: int = 6,
) -> None:
    box_h = min(INTERNAL_H - y - 4, 8 + max_lines * 11)
    box = pygame.Surface((INTERNAL_W - 12, box_h), pygame.SRCALPHA)
    pygame.draw.rect(box, (10, 12, 20, 210), box.get_rect())
    pygame.draw.rect(box, (*SMOG_GRAY, 160), box.get_rect(), 1)
    # cyan accent tick
    pygame.draw.rect(box, (*NEON_CYAN, 180), (0, 0, 2, box_h))
    surface.blit(box, (6, y))
    for i, line in enumerate(lines[:max_lines]):
        font = serif if line.startswith('"') or line.startswith("…") or len(line) > 28 else mono
        color = REPLICANT_AMBER if line.startswith("[") else WET_WHITE
        if line.startswith("…"):
            color = (140, 160, 180)
        if line.startswith("clerk:"):
            color = NEON_CYAN
        rendered = font.render(line[:48], True, color)
        surface.blit(rendered, (12, y + 6 + i * 11))


def draw_player(surface: pygame.Surface, x: int, y: int, *, frame: int = 0) -> None:
    # trench-coat silhouette + neon edge
    sway = 1 if (frame // 8) % 2 == 0 else 0
    body = pygame.Surface((10, 14), pygame.SRCALPHA)
    pygame.draw.rect(body, (18, 28, 38, 255), (2, 3, 6, 10))  # coat
    pygame.draw.rect(body, (8, 12, 18, 255), (3, 0, 4, 4))  # head
    pygame.draw.rect(body, (*NEON_CYAN, 200), (2, 3, 6, 10), 1)
    pygame.draw.rect(body, WET_WHITE, (4, 1, 2, 2))  # eyes / wet glint
    # cigarette ember when standing
    if frame % 20 < 10:
        pygame.draw.circle(body, REPLICANT_AMBER, (9, 5), 1)
    surface.blit(body, (x - sway, y - 2))


def _draw_building(
    surface: pygame.Surface,
    x: int,
    y: int,
    w: int,
    h: int,
    *,
    shade: tuple[int, int, int],
    lit: bool = True,
    frame: int = 0,
) -> None:
    pygame.draw.rect(surface, shade, (x, y, w, h))
    pygame.draw.line(surface, (shade[0] + 8, shade[1] + 8, shade[2] + 10), (x, y), (x + w, y), 1)
    if not lit:
        return
    cols = max(1, (w - 6) // 10)
    rows = max(1, (h - 10) // 12)
    for row in range(rows):
        for col in range(cols):
            wx = x + 4 + col * 10
            wy = y + 6 + row * 12
            on = ((frame // 20) + row * 3 + col * 7) % 11 != 0
            if on:
                glow = REPLICANT_AMBER if (row + col) % 5 == 0 else (40, 70, 90)
                pygame.draw.rect(surface, glow, (wx, wy, 5, 6))
            else:
                pygame.draw.rect(surface, (22, 24, 32), (wx, wy, 5, 6))


def draw_alley(surface: pygame.Surface, graffiti: str = "", *, frame: int = 0) -> None:
    # smog sky gradient
    for gy in range(0, 90):
        t = gy / 90
        r = int(10 + t * 8)
        g = int(10 + t * 6)
        b = int(18 + t * 16)
        pygame.draw.line(surface, (r, g, b), (0, gy), (INTERNAL_W, gy))

    # distant skyline
    for i, (bx, bw, bh) in enumerate(((8, 28, 40), (50, 36, 55), (100, 22, 35), (140, 40, 60), (200, 30, 45), (250, 45, 70), (300, 24, 38))):
        shade = (16 + (i % 3) * 3, 16 + (i % 2) * 2, 24 + (i % 4) * 2)
        _draw_building(surface, bx, 90 - bh, bw, bh, shade=shade, lit=(i % 2 == 0), frame=frame)

    # mid / near buildings
    _draw_building(surface, 0, 40, 110, 120, shade=(18, 18, 28), frame=frame)
    _draw_building(surface, 130, 50, 100, 110, shade=(22, 22, 34), frame=frame + 5)
    _draw_building(surface, 240, 35, 90, 125, shade=(16, 18, 26), frame=frame + 2)

    # hanging cables
    for cx0, cx1, cy in ((20, 140, 48), (150, 280, 42), (60, 220, 58)):
        mid = (cx0 + cx1) // 2
        pygame.draw.lines(
            surface,
            (35, 40, 50),
            False,
            [(cx0, cy), (mid, cy + 8), (cx1, cy + 2)],
            1,
        )

    # wet street
    pygame.draw.rect(surface, (12, 14, 20), (0, 145, INTERNAL_W, 35))
    pygame.draw.line(surface, (28, 34, 48), (0, 145), (INTERNAL_W, 145), 1)

    # puddles with neon bleed
    puddles = ((36, 152, 34, 7), (118, 156, 40, 6), (210, 150, 28, 8), (270, 158, 32, 6))
    for px, py, pw, ph in puddles:
        pygame.draw.ellipse(surface, PUDDLE, (px, py, pw, ph))
        tint = NEON_CYAN if (px + frame) % 60 < 30 else REPLICANT_AMBER
        pygame.draw.ellipse(surface, (*tint, ), (px + 4, py + 1, max(4, pw - 10), max(2, ph - 3)))
        # soften tint by overlaying dark
        soft = pygame.Surface((pw, ph), pygame.SRCALPHA)
        pygame.draw.ellipse(soft, (0, 0, 0, 140), (0, 0, pw, ph))
        surface.blit(soft, (px, py))

    # doorway + warm interior spill
    pygame.draw.rect(surface, (24, 28, 40), (268, 88, 34, 58))
    spill = pygame.Surface((40, 60), pygame.SRCALPHA)
    pygame.draw.rect(spill, (255, 140, 40, 40), (0, 0, 40, 60))
    surface.blit(spill, (266, 88))
    pygame.draw.rect(surface, (8, 40, 48), (276, 108, 16, 36))
    # cigarette glow in doorway
    ember = 2 + (1 if frame % 16 < 8 else 0)
    pygame.draw.circle(surface, REPLICANT_AMBER, (284, 118), ember)
    glow = pygame.Surface((12, 12), pygame.SRCALPHA)
    pygame.draw.circle(glow, (255, 154, 60, 60), (6, 6), 5)
    surface.blit(glow, (278, 112))

    if graffiti:
        font = pygame.font.SysFont("consolas,courier,monospace", 6)
        tag = font.render(graffiti[:28], True, BLOOD_NEON)
        surface.blit(tag, (48, 118))
        # drip
        pygame.draw.line(surface, (*BLOOD_NEON, ), (50, 126), (50, 132), 1)


def _draw_photo_variant(surface: pygame.Surface, x: int, y: int, variant: int, alpha: int = 255) -> None:
    frame = pygame.Surface((22, 16), pygame.SRCALPHA)
    base = (42, 32, 24, alpha)
    accent = (REPLICANT_AMBER[0], REPLICANT_AMBER[1], REPLICANT_AMBER[2], alpha)
    highlight = (WET_WHITE[0], WET_WHITE[1], WET_WHITE[2], min(255, alpha + 40))
    rain = (70, 90, 110, alpha)

    # photo border
    pygame.draw.rect(frame, (20, 16, 14, alpha), (0, 0, 22, 16))
    pygame.draw.rect(frame, base, (1, 1, 20, 14))

    if variant == 0:
        # woman turning away
        pygame.draw.circle(frame, accent, (14, 5), 3)
        pygame.draw.polygon(frame, (60, 40, 30, alpha), [(14, 8), (8, 15), (18, 15)])
        pygame.draw.line(frame, highlight, (12, 6), (16, 5), 1)
        pygame.draw.line(frame, rain, (2, 3), (4, 12), 1)
    elif variant == 1:
        # empty street
        pygame.draw.line(frame, (55, 65, 80, alpha), (2, 11), (20, 11), 1)
        pygame.draw.rect(frame, (30, 35, 45, alpha), (3, 3, 7, 8))
        pygame.draw.rect(frame, (28, 32, 42, alpha), (13, 4, 6, 7))
        pygame.draw.line(frame, (*NEON_CYAN, min(255, alpha)), (4, 5), (8, 5), 1)
    else:
        # wrong self
        pygame.draw.rect(frame, base, (4, 2, 14, 12))
        pygame.draw.circle(frame, (70, 55, 45, alpha), (11, 6), 4)
        pygame.draw.line(frame, (200, 80, 80, alpha), (8, 6), (8, 6), 1)
        pygame.draw.line(frame, (200, 80, 80, alpha), (14, 6), (14, 6), 1)
        pygame.draw.arc(frame, accent, (7, 8, 8, 5), 3.4, 6.0, 1)

    surface.blit(frame, (x, y))


def draw_room(
    surface: pygame.Surface,
    frame: int,
    photo_weights: tuple[float, float, float],
    *,
    photo_phase: bool = False,
    collapsed_variant: int | None = None,
) -> None:
    # wall + floor
    for gy in range(INTERNAL_H):
        t = gy / INTERNAL_H
        c = (int(10 + t * 4), int(10 + t * 3), int(16 + t * 6))
        pygame.draw.line(surface, c, (0, gy), (INTERNAL_W, gy))

    # rain-streaked window
    pygame.draw.rect(surface, (14, 20, 30), (18, 28, 70, 50))
    pygame.draw.rect(surface, SMOG_GRAY, (18, 28, 70, 50), 1)
    for i in range(6):
        sx = 24 + i * 10
        pygame.draw.line(surface, (40, 55, 70), (sx, 32), (sx - 2, 74), 1)
    # cyan bleed through glass
    glass = pygame.Surface((66, 46), pygame.SRCALPHA)
    glass.fill((0, 180, 200, 18 + (frame % 20)))
    surface.blit(glass, (20, 30))

    # table
    pygame.draw.rect(surface, (32, 26, 22), (48, 88, 224, 12))
    pygame.draw.rect(surface, (22, 18, 16), (56, 100, 8, 28))
    pygame.draw.rect(surface, (22, 18, 16), (256, 100, 8, 28))

    # desk lamp glow cone
    cone = pygame.Surface((80, 50), pygame.SRCALPHA)
    pygame.draw.polygon(cone, (255, 180, 80, 28), [(40, 0), (0, 50), (80, 50)])
    surface.blit(cone, (120, 48))
    pygame.draw.rect(surface, (50, 45, 40), (156, 44, 6, 16))
    pygame.draw.ellipse(surface, REPLICANT_AMBER, (150, 40, 18, 8))
    draw_neon_glow(surface, (150, 40, 18, 8), REPLICANT_AMBER, layers=2)

    # photo plate under lamp
    pygame.draw.rect(surface, REPLICANT_AMBER, (148, 74, 28, 22), 1)
    pygame.draw.rect(surface, (28, 22, 16), (150, 76, 24, 18))

    ox = frame % 3 - 1
    if collapsed_variant is not None:
        _draw_photo_variant(surface, 151 + ox, 77, collapsed_variant)
    elif photo_phase:
        from timeline_rental.quantum.photo import glitch_variant

        primary = glitch_variant(frame, photo_weights)
        secondary = (primary + 1) % 3
        blink = frame % 12 < 6
        _draw_photo_variant(surface, 151 + (0 if blink else 1), 77, primary, 255 if blink else 190)
        _draw_photo_variant(surface, 151 + (1 if blink else 0), 76, secondary, 80)
        # glitch scan
        if frame % 7 == 0:
            pygame.draw.line(surface, NEON_CYAN, (150, 78 + (frame % 14)), (174, 78 + (frame % 14)), 1)
    else:
        v = (frame // 6) % 3
        _draw_photo_variant(surface, 151 + ox, 77, v, 150)

    # examiner silhouette — calm, watching
    pygame.draw.rect(surface, (28, 30, 38), (230, 48, 16, 36))
    pygame.draw.circle(surface, (36, 38, 48), (238, 44), 6)
    # cigarette
    pygame.draw.circle(surface, (255, 120, 40), (246, 56), 1 + (frame % 18 < 9))

    # whiskey glass
    pygame.draw.rect(surface, (50, 40, 30), (68, 80, 8, 12), 1)
    pygame.draw.rect(surface, (120, 80, 30), (69, 86, 6, 5))

    # floor wet reflection strip
    refl = pygame.Surface((INTERNAL_W, 20), pygame.SRCALPHA)
    refl.fill((0, 40, 50, 25))
    surface.blit(refl, (0, 148))


def draw_collapse_flash(surface: pygame.Surface, strength: float) -> None:
    overlay = pygame.Surface((INTERNAL_W, INTERNAL_H), pygame.SRCALPHA)
    alpha = int(220 * strength)
    overlay.fill((255, 154, 60, alpha))
    surface.blit(overlay, (0, 0))
    # brief cyan edge
    if strength > 0.5:
        pygame.draw.rect(overlay, (*NEON_CYAN, 80), (0, 0, INTERNAL_W, INTERNAL_H), 3)
        surface.blit(overlay, (0, 0))


def draw_store(surface: pygame.Surface, mono: pygame.font.Font, frame: int, flicker: bool) -> None:
    surface.fill((8, 8, 14))
    # ceiling gloom gradient
    for gy in range(36):
        pygame.draw.line(surface, (10 + gy // 4, 10, 16 + gy // 3), (0, gy), (INTERNAL_W, gy))

    # shelves with tape spines
    spine_colors = (
        SMOG_GRAY,
        (40, 50, 70),
        (60, 30, 40),
        (30, 55, 50),
        (50, 45, 30),
    )
    for si, sx in enumerate((8, 88, 168, 248)):
        pygame.draw.rect(surface, (18, 18, 28), (sx, 36, 56, 100))
        pygame.draw.rect(surface, SMOG_GRAY, (sx, 36, 56, 100), 1)
        for row in range(5):
            for col in range(4):
                c = spine_colors[(si + row + col) % len(spine_colors)]
                pygame.draw.rect(surface, c, (sx + 4 + col * 12, 42 + row * 16, 9, 12))
                pygame.draw.line(surface, (c[0] + 20, c[1] + 20, c[2] + 20), (sx + 5 + col * 12, 44 + row * 16), (sx + 11 + col * 12, 44 + row * 16), 1)

    # CRT — static that almost resolves into a face
    crt_x, crt_y = 108, 48
    pygame.draw.rect(surface, (20, 20, 28), (crt_x - 4, crt_y - 4, 112, 70))
    pygame.draw.rect(surface, (12, 12, 18), (crt_x, crt_y, 104, 58))
    static = pygame.Surface((96, 50), pygame.SRCALPHA)
    for _ in range(40):
        px = (_ * 17 + frame * 3) % 96
        py = (_ * 11 + frame * 5) % 46
        shade = 50 + ((_ * 13 + frame) % 80)
        pygame.draw.line(static, (shade, shade + 10, shade + 20, 180), (px, py), (px + 3, py), 1)
    # ghost face in static
    if frame % 40 < 12:
        pygame.draw.circle(static, (180, 190, 200, 50), (48, 22), 10)
        pygame.draw.circle(static, (20, 20, 30, 80), (44, 20), 2)
        pygame.draw.circle(static, (20, 20, 30, 80), (52, 20), 2)
    surface.blit(static, (crt_x + 4, crt_y + 4))
    border = NEON_CYAN if flicker else SMOG_GRAY
    pygame.draw.rect(surface, border, (crt_x, crt_y, 104, 58), 1)

    # glowing damaged tape on front shelf
    glow = NEON_CYAN if flicker else REPLICANT_AMBER
    draw_neon_glow(surface, (12, 48, 48, 22), glow, layers=3)
    pygame.draw.rect(surface, (18, 18, 28), (12, 48, 48, 22))
    pygame.draw.rect(surface, glow, (12, 48, 48, 22), 1)
    tape_label = mono.render("BLADE RUNNER", True, glow)
    surface.blit(tape_label, (14, 50))
    dmg = mono.render("[damaged]", True, REPLICANT_AMBER)
    surface.blit(dmg, (14, 60))

    # locked / missing tapes
    for i, (name, status) in enumerate((("CASABLANCA", "[missing]"), ("VERTIGO", "[rewinding]"))):
        y = 78 + i * 20
        label = mono.render(name, True, SMOG_GRAY)
        surface.blit(label, (178, y))
        lock = mono.render(status, True, (50, 55, 65))
        surface.blit(lock, (178, y + 8))

    # counter strip
    pygame.draw.rect(surface, (24, 22, 30), (0, 140, INTERNAL_W, 8))
    pygame.draw.line(surface, NEON_DIM, (0, 140), (INTERNAL_W, 140), 1)

    # signage
    sign_color = NEON_CYAN if flicker else NEON_DIM
    sign = mono.render("TIMELINE RENTAL", True, sign_color)
    draw_neon_glow(
        surface,
        (INTERNAL_W // 2 - sign.get_width() // 2 - 2, 6, sign.get_width() + 4, 12),
        sign_color,
        layers=2,
    )
    surface.blit(sign, (INTERNAL_W // 2 - sign.get_width() // 2, 8))
    open_label = mono.render("OPEN 24h (maybe)", True, SMOG_GRAY)
    surface.blit(open_label, (INTERNAL_W // 2 - open_label.get_width() // 2, 20))


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
