
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

"""About screen displayed in the demo and selected from the main menu."""

import sys

import pygame

from demo.colors import Colors
from demo.resources import Resources
from demo.screen import Screen


class AboutScreen(Screen):
    """About screen displayed in the demo."""

    # colors used on about screen
    TITLE_COLOR = (255, 255, 255)
    AUTHOR_COLOR = (120, 120, 255)
    WORK_COLOR = (120, 120, 120)

    def __init__(self, display: pygame.Surface, resources: Resources) -> None:
        """Initialize the about screen."""
        super(AboutScreen, self).__init__(display, resources, "About")

        # fonts and other required resources are taken from resources object.

        # pre-render other texts
        self._author1 = self._resources.normalFont.render(
            "Pavel", True, AboutScreen.AUTHOR_COLOR, AboutScreen.BACKGROUND_COLOR
        )

        self._work1 = self._resources.normalFont.render(
            "code", True, AboutScreen.WORK_COLOR, AboutScreen.BACKGROUND_COLOR
        )

        # version info texts
        pygame_version = f"Pygame version: {pygame.version.ver}"
        self._pygame_version = self._resources.smallFont.render(
            pygame_version, True, AboutScreen.WORK_COLOR, AboutScreen.BACKGROUND_COLOR
        )

        sdlVer = f"{pygame.version.SDL.major}.{pygame.version.SDL.minor}.{pygame.version.SDL.patch}"
        self._sdl_version = self._resources.smallFont.render(
            "SDL version: " + sdlVer,
            True,
            AboutScreen.WORK_COLOR,
            AboutScreen.BACKGROUND_COLOR,
        )
        pv = sys.version_info
        pythonVersion = f"{pv.major}.{pv.minor}.{pv.micro} {pv.releaselevel}"
        self._python_version = self._resources.smallFont.render(
            "Python version: " + pythonVersion,
            True,
            AboutScreen.WORK_COLOR,
            AboutScreen.BACKGROUND_COLOR,
        )

        self._clock = pygame.time.Clock()
        self._photo1 = self._resources.images["authors1"]

    def draw(self) -> None:
        """Draw about screen."""
        self._display.fill(Colors.BLACK.value)
        self.drawTitle()
        self.drawAuthors()
        self.drawTexts()
        self.drawVersionInfo()

    def drawAuthors(self) -> None:
        """Draw authors photos onto the screen."""
        self._display.blit(self._photo1, (100, 350))

    def drawTexts(self) -> None:
        """Draw texts onto the screen."""
        self._display.blit(self._author1, (250, 340))
        self._display.blit(self._work1, (250, 380))

    def drawVersionInfo(self) -> None:
        """Draw info about library versions onto the screen."""
        x = 700
        y = 675
        step = 25
        self._display.blit(self._python_version, (x, y))
        self._display.blit(self._pygame_version, (x, y + step))
        self._display.blit(self._sdl_version, (x, y + step * 2))

    def eventLoop(self) -> int:
        """Event loop for About screen that just waits for keypress or window close operation."""
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

            # all events has been processed - update scene and redraw the screen
            self.draw()
            pygame.display.update()
            self._clock.tick(25)
