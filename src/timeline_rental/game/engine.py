"""Main pygame loop — neon noir at 320×180."""

from __future__ import annotations

import os
import random
import sys

import pygame

from timeline_rental.data.db import init_db
from timeline_rental.game.constants import (
    DEFAULT_SCALE,
    INTERNAL_H,
    INTERNAL_W,
    RAIN_BLACK,
)
from timeline_rental.game.render import Rain, draw_collapse_flash, load_fonts
from timeline_rental.game.scenes import (
    AlleyScene,
    IntroScene,
    ReceiptScene,
    RoomScene,
    StoreScene,
)
from timeline_rental.game.state import GameState


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Timeline Rental")
        self.scale = int(os.getenv("WINDOW_SCALE", DEFAULT_SCALE))
        self.window = pygame.display.set_mode(
            (INTERNAL_W * self.scale, INTERNAL_H * self.scale)
        )
        self.canvas = pygame.Surface((INTERNAL_W, INTERNAL_H))
        self.clock = pygame.time.Clock()
        self.mono, self.serif = load_fonts()
        self.rain = Rain()
        self.state = GameState(seed=random.randint(0, 2**31 - 1))
        init_db()
        self.scenes = {
            "store": StoreScene(),
            "intro": IntroScene(),
            "alley": AlleyScene(),
            "room": RoomScene(),
        }
        self.current_name = "store"
        self.running = True

    @property
    def current(self):
        return self.scenes[self.current_name]

    def _fresh_scene(self, name: str):
        factories = {
            "store": StoreScene,
            "intro": IntroScene,
            "alley": AlleyScene,
            "room": RoomScene,
        }
        if name in factories:
            self.scenes[name] = factories[name]()

    def switch(self, name: str) -> None:
        if name == "quit":
            self.running = False
            return
        if name == "receipt":
            self.scenes["receipt"] = ReceiptScene(self.state)
            self.current_name = "receipt"
            return
        if name in {"store", "intro", "alley", "room"}:
            self._fresh_scene(name)
        self.current_name = name

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            flicker = random.random() > 0.07

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    nxt = self.current.handle_event(event, self.state)
                    if nxt:
                        self.switch(nxt)

            if self.state.flash_frames > 0:
                self.state.flash_frames -= 1

            nxt = self.current.update(dt, self.state)
            if nxt:
                self.switch(nxt)

            self.rain.update()
            self.canvas.fill(RAIN_BLACK)
            self.current.draw(self.canvas, self.mono, self.serif, self.rain, flicker)

            if self.state.flash_frames > 0:
                draw_collapse_flash(self.canvas, self.state.flash_frames / 3)

            scaled = pygame.transform.scale(
                self.canvas,
                (INTERNAL_W * self.scale, INTERNAL_H * self.scale),
            )
            self.window.blit(scaled, (0, 0))
            pygame.display.flip()

        pygame.quit()


def main() -> None:
    GameEngine().run()
    sys.exit(0)
