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

"""Entry point to initialization part + entry to the main event loop."""

import sys

import pygame
import pygame.locals

from demo.main_menu import MainMenu
from demo.ghost import Ghost
from demo.config import loadConfiguration
from demo.colors import Colors
from demo.splash_screen import SplashScreen
from demo.textures_screen import TexturesScreen
from demo.textures_menu import TexturesMenu
from demo.cplx_screen import CplxScreen
from demo.strange_attractors_screen import StrangeAttractorsScreen
from demo.ifs_screen import IteratedFunctionsSystemsScreen
from demo.dynamic_systems_screen import DynamicSystemsScreen
from demo.about_screen import AboutScreen
from demo.resources import Resources

import textures.circle_like_patterns


configuration = loadConfiguration("demo.ini")

pygame.init()
resources = Resources(configuration)

clock = pygame.time.Clock()

# create demo window
window_width = int(configuration["screen"]["window_width"])
window_height = int(configuration["screen"]["window_height"])
display = pygame.display.set_mode([window_width, window_height])

# set window title
pygame.display.set_caption("Procedural graphics demos")

display.fill(Colors.BLACK.value)

red_ghost = Ghost(display, resources, "ghost_red")

splash_screen = SplashScreen(display, resources, "splash_screen", 8, red_ghost)

def main() -> None:
    while True:
        menuItem = splash_screen.eventLoop()
        if menuItem == MainMenu.QUIT.value:
            pygame.quit()
            sys.exit()


main()

# finito
