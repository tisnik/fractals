
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

"""Ghost class that represents any ghost in the demo."""

import pygame

from demo.direction import Direction
from demo.resources import Resources
from demo.sprite import Sprite


class Ghost(Sprite):
    """Ghost class that represents any ghost in the demo."""

    def __init__(
        self, surface: pygame.Surface, resources: Resources, filename_prefix: str
    ) -> None:
        """Ghost object initialization, including resource loading."""
        super(Ghost, self).__init__(surface)

        self._scared = False
        self._scared_tick = 0

        self._sprites: dict[Direction, pygame.Surface] = {}
        self._sprites[Direction.LEFT] = resources.images[filename_prefix + "_left"]
        self._sprites[Direction.RIGHT] = resources.images[filename_prefix + "_right"]
        self._sprites[Direction.UP] = resources.images[filename_prefix + "_up"]
        self._sprites[Direction.DOWN] = resources.images[filename_prefix + "_down"]

    def setScared(self, scared: bool) -> None:
        """Set 'scared ghost' mode."""
        self._scared = scared

    def draw(self) -> None:
        """Draw ghost onto the screen or onto surface selected during initialization."""
        self._surface.blit(self._sprites[self._direction], (self._x, self._y))
