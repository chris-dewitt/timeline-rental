"""Smoke-test scene renders — ensures draw paths don't crash."""

from __future__ import annotations

import os

import pygame

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


def test_render_scenes_to_surface():
    pygame.init()
    pygame.display.set_mode((1, 1))
    from timeline_rental.game.render import (
        Rain,
        draw_alley,
        draw_neon_sign,
        draw_player,
        draw_room,
        draw_scanlines,
        draw_store,
        draw_vignette,
        load_fonts,
    )

    canvas = pygame.Surface((320, 180))
    mono, serif = load_fonts()
    rain = Rain(40)

    draw_store(canvas, mono, frame=12, flicker=True)
    rain.draw(canvas)
    draw_scanlines(canvas)
    draw_vignette(canvas)

    draw_alley(canvas, "test graffiti", frame=30)
    draw_neon_sign(canvas, mono, "NEXUS REPAIR", True)
    draw_player(canvas, 40, 132, frame=8)
    rain.update()
    rain.draw(canvas)

    draw_room(canvas, 20, (0.5, 0.3, 0.2), photo_phase=True)
    draw_room(canvas, 20, (0.2, 0.5, 0.3), collapsed_variant=1)

    assert canvas.get_at((10, 10))  # touched pixels
    pygame.quit()
