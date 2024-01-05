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

"""Splash screen with title, welcome animation, and a main menu."""

import pygame

from demo.abstract_menu_screen import AbstractMenuScreen
from demo.colors import Colors
from demo.resources import Resources
from demo.ghost import Ghost


class SplashScreen(AbstractMenuScreen):
    """Splash screen with title, welcome animation, and a main menu."""

    # colors used on splash screen (background color is read from Screen class
    CREDITS_COLOR = (140, 140, 140)

    def __init__(self, display: pygame.Surface, resources: Resources,
            filename_prefix: str, frames_count: int, ghost: Ghost) -> None:
        """Initialize the splash screen."""
        super(SplashScreen, self).__init__(display, resources, ghost, "Procedural graphics demos")

        # pre-render all menu items onto surfaces
        self._menu = (
            self.renderMenuItem("Procedural textures"),
            self.renderMenuItem("Fractals in complex plane"),
            self.renderMenuItem("Strange attractors"),
            self.renderMenuItem("Iterated function systems"),
            self.renderMenuItem("Dynamic systems"),
            self.renderMenuItem("About"),
            self.renderMenuItem("Quit"),
        )

        credits = "2023 Pavel Tišnovský"
        self._credits = self._resources.smallFont.render(credits,
                                                         True,
                                                         SplashScreen.CREDITS_COLOR,
                                                         SplashScreen.BACKGROUND_COLOR)
        # retrieve icons
        self._barnsley_icon = self._resources.images["main_barnsley"]
        self._mandelbrot_icon = self._resources.images["main_mandelbrot"]
        self._dynamic_icon = self._resources.images["main_dynamic"]
        self._ifs_icon = self._resources.images["main_ifs"]

    def draw(self) -> None:
        """Draw splash screen."""
        self._display.fill(Colors.BLACK.value)
        self.drawTitle()
        self.drawMenu()
        self.drawGhost()
        self.drawCredits()
        self.drawIcons()

    def drawCredits(self) -> None:
        """Draw credits."""
        x = self._display.get_width() - self._credits.get_width() - 10
        y = self._display.get_height() - 30
        self._display.blit(self._credits, (x, y))

    def drawIcons(self) -> None:
        """Draw icons."""
        self._display.blit(self._barnsley_icon, (100, 140))
        self._display.blit(self._mandelbrot_icon, (320, 140))
        self._display.blit(self._dynamic_icon, (540, 140))
        self._display.blit(self._ifs_icon, (760, 140))
