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

"""Setup screen."""

import pygame

from demo.abstract_menu_screen import AbstractMenuScreen
from demo.resources import Resources
from demo.ghost import Ghost


class SetupScreen(AbstractMenuScreen):
    """Setup screen."""

    def __init__(
        self, display: pygame.Surface, resources: Resources, ghost: Ghost
    ) -> None:
        """Initialize the screen."""
        super(SetupScreen, self).__init__(
            display, resources, ghost, "Fractals in complex plane"
        )

        # pre-render all menu items onto surfaces
        self._menu = (
            self.renderMenuItem("Use Python renderers"),
            self.renderMenuItem("Use C/native renderers"),
            self.renderMenuItem("Return to main screen"),
        )

        # retrieve icons
        self._python_logo = self._resources.images["python_logo"]
        self._c_logo = self._resources.images["c_logo"]

    def drawIcons(self) -> None:
        """Draw icons."""
        self._display.blit(self._python_logo, (320, 140))
        self._display.blit(self._c_logo, (540, 140))
