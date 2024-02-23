# vim: set fileencoding=utf-8

#
#  (C) Copyright 2023, 2024  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#

"""Textures screen."""

import pygame

from demo.abstract_menu_screen import AbstractMenuScreen
from demo.resources import Resources
from demo.ghost import Ghost


class TexturesScreen(AbstractMenuScreen):
    """Textures screen."""

    def __init__(
        self, display: pygame.Surface, resources: Resources, ghost: Ghost
    ) -> None:
        """Initialize the screen."""
        super(TexturesScreen, self).__init__(
            display, resources, ghost, "Procedural textures"
        )

        # pre-render all menu items onto surfaces
        self._menu = (
            self.renderMenuItem("Circle moiré patterns"),
            self.renderMenuItem("Other moiré patterns"),
            self.renderMenuItem("Plasma"),
            self.renderMenuItem("FM-synth"),
            self.renderMenuItem("Return to main screen"),
        )

        # retrieve icons
        self._circles_icon = self._resources.images["procedural_circles"]
        self._plasma_icon = self._resources.images["procedural_plasma"]
        self._greens_icon = self._resources.images["procedural_greens"]
        self._fm_icon = self._resources.images["procedural_fm"]

    def drawIcons(self) -> None:
        """Draw icons."""
        self._display.blit(self._circles_icon, (100, 140))
        self._display.blit(self._greens_icon, (320, 140))
        self._display.blit(self._plasma_icon, (540, 140))
        self._display.blit(self._fm_icon, (760, 140))
