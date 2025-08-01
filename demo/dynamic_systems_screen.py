
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

"""Dynamic system screen."""

import pygame

from demo.abstract_menu_screen import AbstractMenuScreen
from demo.ghost import Ghost
from demo.resources import Resources


class DynamicSystemsScreen(AbstractMenuScreen):
    """Dynamic systems screen."""

    def __init__(
        self, display: pygame.Surface, resources: Resources, ghost: Ghost
    ) -> None:
        """Initialize the screen."""
        super(DynamicSystemsScreen, self).__init__(
            display, resources, ghost, "Dynamic Systems"
        )

        # pre-render all menu items onto surfaces
        self._menu = (self.renderMenuItem("Return to main screen"),)
