# vim: set fileencoding=utf-8

#
#  (C) Copyright 2024  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#

"""Circle moire screen."""

import pygame
import sys
from PIL import Image

from demo.screen import Screen
from demo.colors import Colors

from demo.resources import Resources
from pygame.surface import Surface
from textures.circle_like_patterns import recalc_any_pattern


class OtherMoireScreen(Screen):
    # rendered image size
    IMAGE_WIDTH = 512
    IMAGE_HEIGHT = 512

    FUNCTIONS = [
        lambda x, y: x * x + y * y,
        lambda x, y: x * x - y * y,
        lambda x, y: x**3 + y**3,
        lambda x, y: x**4 + y**4,
        lambda x, y: x * x + y * y + x * y * 1.5,
        lambda x, y: x * x * y + y * y * x,
    ]

    RELATIVE_ZOOMS = [32 + 75, 32 + 75, 15, 15, 60, 15]

    def __init__(self, display: Surface, resources: Resources, title_text: str) -> None:
        status = "← zoom out   → zoom in   [F]unction   [P]alette   Esc back"
        super(OtherMoireScreen, self).__init__(display, resources, title_text, status)
        self._clock = pygame.time.Clock()
        self._palette_index = 0
        self._zoom_index = 0
        self._renderer = recalc_any_pattern
        self._function = 0
        self._zoom = 2.25
        self._image = self.calcImage()

    def calcImage(self) -> Surface:
        threshold = (
            self._zoom * OtherMoireScreen.RELATIVE_ZOOMS[self._function]
        )  # (2 << 5) + 50.0 * self._zoom
        image = Image.new(
            "RGB", (OtherMoireScreen.IMAGE_WIDTH, OtherMoireScreen.IMAGE_HEIGHT)
        )
        palette = self._resources.palettes[self._palette_index]
        self._renderer(
            image,
            palette,
            -threshold,
            -threshold,
            threshold,
            threshold,
            OtherMoireScreen.FUNCTIONS[self._function],
        )
        return pygame.image.fromstring(
            image.tobytes(), image.size, image.mode
        ).convert()

    def draw(self) -> None:
        """Draw screen."""
        self._display.fill(Colors.BLACK.value)
        self.drawTitle()
        self.drawStatus()
        x = self._display.get_width() / 2 - OtherMoireScreen.IMAGE_WIDTH / 2
        y = 100
        self._display.blit(self._image, (x, y))

    def eventLoop(self) -> int:
        """Event loop for splash screen that just waits for keypress or window close action."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.locals.KEYDOWN:
                    if event.key == pygame.locals.K_ESCAPE:
                        return
                    if event.key == pygame.locals.K_LEFT:
                        self._zoom *= 1.5
                        self._image = self.calcImage()
                    if event.key == pygame.locals.K_RIGHT:
                        self._zoom /= 1.5
                        self._image = self.calcImage()
                    if event.key == pygame.locals.K_f:
                        self._function += 1
                        if self._function == len(OtherMoireScreen.FUNCTIONS):
                            self._function = 0
                        self._image = self.calcImage()
                    if event.key == pygame.locals.K_p:
                        self._palette_index += 1
                        if self._palette_index >= len(self._resources.palettes):
                            self._palette_index = 0
                        self._image = self.calcImage()

            # all events has been processed - redraw the screen
            self.draw()
            pygame.display.update()
            self._clock.tick(8)
