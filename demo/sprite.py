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

"""Super class for all movable objects on the scene."""

from abc import ABC, abstractmethod
from typing import Tuple

import pygame

from demo.direction import Direction


class Sprite(ABC):
    """Super class for all movable objects in the demo."""

    def __init__(self, surface: pygame.Surface) -> None:
        """Initialize the sprite."""
        # most sprites can be rotated in four directions
        self._direction = Direction.RIGHT

        # absolute position of sprite on screen
        self._x = 0
        self._y = 0

        # surface used to display the sprite
        self._surface = surface

    @abstractmethod
    def draw(self) -> None:
        """Elementary draw method to be overwritten in derived classes."""
        pass

    def setDirection(self, direction: Direction) -> None:
        """Set sprite direction (if applicable)."""
        self._direction = direction

    def cycleDirection(self) -> None:
        """Rotate the sprite by switching to the next possible direction."""
        self._direction = self._direction.succ()

    def setPosition(self, x: int, y: int) -> None:
        """Set sprite position."""
        self._x = x
        self._y = y

    def getPosition(self) -> Tuple[int, int]:
        """Get sprite position."""
        return (self._x, self._y)
