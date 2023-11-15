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

# Nutno importovat kvůli konstantám QUIT atd.
from pygame.locals import QUIT, K_ESCAPE, KEYDOWN

from demo.main_menu import MainMenu
from demo.ghost import Ghost
from demo.config import loadConfiguration
from demo.colors import Colors

configuration = loadConfiguration("demo.ini")

import textures.circle_like_patterns
import textures.circle_moire_no_palette
import textures.circle_moire_with_palette

# Velikost okna aplikace
WIDTH = 256
HEIGHT = 256

# Inicializace knihovny Pygame
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


# Získání dvourozměrného pole s hodnotami pixelů
pixelArray = pygame.PixelArray(display)

# Změna barev některých pixelů
for y in range(HEIGHT):
    for x in range(WIDTH):
        pixelArray[x][y] = (x, y, (x + y) % 256)

# Pixely byly změněny, pole je možné odstranit z paměti
# a současně tak uvolnit surface pro další operace
del pixelArray


# Hlavní smyčka
while True:
    # Načtení a zpracování všech událostí z fronty
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(20)

# finito
