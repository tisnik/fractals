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
from demo.cplx_menu import CplxMenu
from demo.strange_attractors_screen import StrangeAttractorsScreen
from demo.ifs_screen import IteratedFunctionsSystemsScreen
from demo.dynamic_systems_screen import DynamicSystemsScreen
from demo.setup_screen import SetupScreen
from demo.about_screen import AboutScreen
from demo.resources import Resources
from demo.circle_moire_screen import CircleMoireScreen
from demo.other_moire_screen import OtherMoireScreen
from demo.plasma_screen import PlasmaScreen
from demo.mandelbrot_screen import MandelbrotScreen


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


def in_texture_screen(display, resources, red_ghost) -> None:
    textures_screen = TexturesScreen(display, resources, red_ghost)
    textures_screen.draw()
    while True:
        choice = textures_screen.eventLoop()
        if choice in {TexturesMenu.QUIT.value, MainMenu.QUIT.value}:
            return
        elif choice == TexturesMenu.CIRCLE_MOIRE.value:
            circle_moire_screen = CircleMoireScreen(
                display, resources, "Circle moire patterns"
            )
            circle_moire_screen.draw()
            circle_moire_screen.eventLoop()
        elif choice == TexturesMenu.OTHER_MOIRE.value:
            other_moire_screen = OtherMoireScreen(
                display, resources, "Other moire patterns"
            )
            other_moire_screen.draw()
            other_moire_screen.eventLoop()
        elif choice == TexturesMenu.PLASMA.value:
            plasma_screen = PlasmaScreen(display, resources, "Plasma")
            plasma_screen.draw()
            plasma_screen.eventLoop()


def in_cplx_screen(display, resources, red_ghost) -> None:
    cplx_screen = CplxScreen(display, resources, red_ghost)
    cplx_screen.draw()
    while True:
        choice = cplx_screen.eventLoop()
        if choice in {CplxMenu.QUIT.value, MainMenu.QUIT.value}:
            return
        elif choice == CplxMenu.MANDELBROT.value:
            mandelbrot_screen = MandelbrotScreen(
                display, resources, "Mandelbrot fractal"
            )
            mandelbrot_screen.draw()
            mandelbrot_screen.eventLoop()


def main() -> None:
    while True:
        menuItem = splash_screen.eventLoop()
        if menuItem == MainMenu.QUIT.value:
            pygame.quit()
            sys.exit()
        elif menuItem == MainMenu.PROCEDURAL_TEXTURES.value:
            in_texture_screen(display, resources, red_ghost)
        elif menuItem == MainMenu.COMPLEX_FRACTALS.value:
            in_cplx_screen(display, resources, red_ghost)
        elif menuItem == MainMenu.STRANGE_ATTRACTORS.value:
            # TODO: refactor a bit
            cplx_screen = StrangeAttractorsScreen(display, resources, red_ghost)
            cplx_screen.draw()
            cplx_screen.eventLoop()
        elif menuItem == MainMenu.IFS.value:
            cplx_screen = IteratedFunctionsSystemsScreen(display, resources, red_ghost)
            cplx_screen.draw()
            cplx_screen.eventLoop()
        elif menuItem == MainMenu.DYNAMIC_SYSTEMS.value:
            cplx_screen = DynamicSystemsScreen(display, resources, red_ghost)
            cplx_screen.draw()
            cplx_screen.eventLoop()
        elif menuItem == MainMenu.ABOUT.value:
            about_screen = AboutScreen(display, resources)
            about_screen.draw()
            about_screen.eventLoop()
        elif menuItem == MainMenu.SETUP.value:
            setup_screen = SetupScreen(display, resources, red_ghost)
            setup_screen.draw()
            setup_screen.eventLoop()


main()

# finito
