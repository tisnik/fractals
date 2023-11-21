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

"""Iterated functions system screen."""

import pygame

from demo.abstract_menu_screen import AbstractMenuScreen
from demo.resources import Resources
from demo.ghost import Ghost


class IteratedFunctionsSystemsScreen(AbstractMenuScreen):
    """Iterated function systems screen."""

    def __init__(self, display: pygame.Surface, resources: Resources,
            ghost: Ghost) -> None:
        """Initialize the screen."""
        super(IteratedFunctionsSystemsScreen, self).__init__(display, resources, ghost, "Iterated Functions Systems")

        # pre-render all menu items onto surfaces
        self._menu = (
            self.renderMenuItem("Return to main screen"),
        )
