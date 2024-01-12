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

"""Superclass for all screens in the demo."""

from abc import ABC
import pygame
import pygame.locals
import sys

from demo.colors import Colors
from demo.resources import Resources


class Screen(ABC):
    """Superclass for all screens in the demo."""

    # colors used on screen
    BACKGROUND_COLOR = Colors.BLACK.value

    # default clock tick
    CLOCK_TICK = 5

    # colors used on menu screen (background color is read from Screen class
    TITLE_COLOR = (255, 255, 255)
    MENU_COLOR = (120, 120, 255)

    def __init__(self, display: pygame.Surface, resources: Resources, title_text: str) -> None:
        """Initialize the screen."""
        # primary display for blitting to screen
        self._display = display

        # all loaded resources
        self._resources = resources

        # clock to be used in event loop
        self._clock = pygame.time.Clock()

        # pre-render demo title
        self._title = self._resources.bigFont.render(title_text, True,
                                                     Screen.TITLE_COLOR,
                                                     Screen.BACKGROUND_COLOR)

    def drawTitle(self) -> None:
        """Draw the title onto splash screen."""
        x = self._display.get_width() / 2 - self._title.get_width() / 2
        y = 0
        self._display.blit(self._title, (x, y))

    def draw(self) -> None:
        """Draw screen."""
        # this method should be overwritten
        self.drawTitle()
        self._display.fill(Screen.BACKGROUND_COLOR)

    def eventLoop(self) -> int:
        """Event loop."""
        # this method should be overwritten
        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.locals.KEYDOWN:
                    if event.key == pygame.locals.K_ESCAPE:
                        return 0
                    if event.key == pygame.locals.K_RETURN:
                        return 0

            # all events has been processed - redraw the screen
            self.draw()
            pygame.display.update()

            # and wait a bit
            self._clock.tick(Screen.CLOCK_TICK)
