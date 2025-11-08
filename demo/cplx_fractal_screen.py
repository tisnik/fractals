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

"""Complex fractal screen."""

import sys

import pygame
from PIL import Image
from pygame.surface import Surface

from demo.colors import Colors
from demo.resources import Resources
from demo.screen import Screen


class CplxFractalScreen(Screen):
    # rendered image size
    # rendered image size
    IMAGE_WIDTH = 512
    IMAGE_HEIGHT = 512

    def __init__(
        self,
        display: Surface,
        resources: Resources,
        title_text: str,
        xmin: float,
        ymin: float,
        xmax: float,
        ymax: float,
        cx: float | None = None,
        cy: float | None = None,
    ) -> None:
        status = "← zoom out   → zoom in   [P]alette   Esc back"
        super(CplxFractalScreen, self).__init__(display, resources, title_text, status)
        self._clock = pygame.time.Clock()
        self._palette_index = 0
        self._renderer = None
        self._cx = cx
        self._cy = cy
        self._xmin = xmin
        self._ymin = ymin
        self._xmax = xmax
        self._ymax = ymax

    def draw(self) -> None:
        """Draw screen."""
        self._display.fill(Colors.BLACK.value)
        self.drawTitle()
        self.drawStatus()
        x = self._display.get_width() / 2 - CplxFractalScreen.IMAGE_WIDTH / 2
        y = 100
        self._display.blit(self._image, (x, y))

    def calcImage(self) -> Surface:
        image = Image.new(
            "RGB", (CplxFractalScreen.IMAGE_WIDTH, CplxFractalScreen.IMAGE_HEIGHT)
        )
        palette = self._resources.palettes[self._palette_index]
        if self._renderer is not None:
            if self._cx is None or self._cy is None:
                self._renderer(
                    image, palette, self._xmin, self._ymin, self._xmax, self._ymax, 500
                )
            else:
                self._renderer(
                    image,
                    palette,
                    self._xmin,
                    self._ymin,
                    self._xmax,
                    self._ymax,
                    self._cx,
                    self._cy,
                    500,
                )
        return pygame.image.fromstring(image.tobytes(), image.size, "RGB").convert()

    def eventLoop(self) -> int:
        """Event loop for splash screen that just waits for keypress or window close action."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.locals.KEYDOWN:
                    if event.key == pygame.locals.K_ESCAPE:
                        return 0
                    if event.key == pygame.locals.K_LEFT:
                        pass
                    if event.key == pygame.locals.K_RIGHT:
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
