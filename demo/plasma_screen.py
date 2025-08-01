
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

"""Plasma screen."""

import sys

import pygame
from PIL import Image
from pygame.surface import Surface

from demo.colors import Colors
from demo.resources import Resources
from demo.screen import Screen
from textures.plasma import spectral_synthesis


class PlasmaScreen(Screen):
    # rendered image size
    IMAGE_WIDTH = 512
    IMAGE_HEIGHT = 512

    def __init__(self, display: Surface, resources: Resources, title_text: str) -> None:
        status = "← zoom out   → zoom in   [P]alette   Esc back"
        super(PlasmaScreen, self).__init__(display, resources, title_text, status)
        self._clock = pygame.time.Clock()
        self._palette_index = 0
        self._image = self.calcImage()

    def calcImage(self) -> Surface:
        image = Image.new("RGB", (PlasmaScreen.IMAGE_WIDTH, PlasmaScreen.IMAGE_HEIGHT))
        palette = self._resources.palettes[self._palette_index]
        spectral_synthesis(image, palette, 4, 0.5)
        return pygame.image.fromstring(
            image.tobytes(), image.size, "RGB"
        ).convert()

    def draw(self) -> None:
        """Draw screen."""
        self._display.fill(Colors.BLACK.value)
        self.drawTitle()
        self.drawStatus()
        x = self._display.get_width() / 2 - PlasmaScreen.IMAGE_WIDTH / 2
        y = 100
        self._display.blit(self._image, (x, y))

    def eventLoop(self) -> int:
        """Event loop for plasma screen that handles user input and renders the plasma effect."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.locals.KEYDOWN:
                    if event.key == pygame.locals.K_ESCAPE:
                        return 0
                    if event.key == pygame.locals.K_LEFT:
                        # TODO: implement zoom out functionality
                        pass
                    if event.key == pygame.locals.K_RIGHT:
                        # TODO: implement zoom in functionality
                        pass
                    if event.key == pygame.locals.K_p:
                        self._palette_index += 1
                        if self._palette_index >= len(self._resources.palettes):
                            self._palette_index = 0
                        self._image = self.calcImage()

            # all events has been processed - redraw the screen
            self.draw()
            pygame.display.update()
            self._clock.tick(8)
