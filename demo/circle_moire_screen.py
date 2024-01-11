# vim: set fileencoding=utf-8

#
#  (C) Copyright 2023  Pavel Tisnovsky
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
from PIL import Image

from demo.screen import Screen
from demo.colors import Colors

import textures.palette_blues as palette_blues
import textures.circle_moire_with_palette as moire


class CircleMoireScreen(Screen):

    # colors used on menu screen (background color is read from Screen class
    TITLE_COLOR = (255, 255, 255)
    MENU_COLOR = (120, 120, 255)

    # rendered image size
    IMAGE_WIDTH = 512
    IMAGE_HEIGHT = 512


    def __init__(self, display, resources, title_text) -> None:
        super(CircleMoireScreen, self).__init__(display, resources)
        self._clock = pygame.time.Clock()

        # pre-render demo title
        self._title = self._resources.bigFont.render(title_text, True,
                                                     Screen.TITLE_COLOR,
                                                     Screen.BACKGROUND_COLOR)
        self._image = self.calcImage()

    def calcImage(self):
        threshold = (2 << 5) + 50 * 2.5
        image = Image.new("RGB", (CircleMoireScreen.IMAGE_WIDTH, CircleMoireScreen.IMAGE_HEIGHT))
        moire.recalc_circle_pattern(image, palette_blues.palette, -threshold, -threshold, threshold, threshold)
        return pygame.image.fromstring(image.tobytes(), image.size, image.mode).convert()

    def drawTitle(self) -> None:
        """Draw the title onto splash screen."""
        x = self._display.get_width() / 2 - self._title.get_width() / 2
        y = 0
        self._display.blit(self._title, (x, y))

    def draw(self) -> None:
        """Draw splash screen."""
        self._display.fill(Colors.BLACK.value)
        self.drawTitle()
        x = self._display.get_width() / 2 - CircleMoireScreen.IMAGE_WIDTH / 2
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

            # all events has been processed - redraw the screen
            self.draw()
            pygame.display.update()
            self._clock.tick(8)
