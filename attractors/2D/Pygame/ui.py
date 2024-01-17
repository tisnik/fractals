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


import sys

import pygame
import pygame.locals
from colors import Colors


def initialize(title, width, height):
    """Initialize Pygame display, drawing surface, and clocks."""
    # set window title
    pygame.display.set_caption(title)

    # initialize window
    display = pygame.display.set_mode([width, height])
    display.fill(Colors.BLACK.value)

    # create all required Pygame objects
    surface = pygame.Surface([width, height])
    surface.fill(Colors.BLACK.value)

    clock = pygame.time.Clock()

    return display, surface, clock


def event_loop(display, surface, clock):
    """Event loop that just waits for keypress or window close operation."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.locals.K_RETURN:
                    pygame.quit()
                    sys.exit()

        # all events has been processed - update scene and redraw the screen
        display.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(25)
