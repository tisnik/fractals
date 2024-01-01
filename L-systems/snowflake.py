#!/usr/bin/env python

import sys
import math

import pygame
import pygame.draw as draw

# Nutno importovat kvůli konstantám QUIT atd.
from pygame.locals import QUIT, K_ESCAPE, KEYDOWN

# Velikost okna aplikace
WIDTH = 800
HEIGHT = 600

# Inicializace knihovny Pygame
pygame.init()

clock = pygame.time.Clock()

# Inicializace okna pro vykreslení fraktálu
display = pygame.display.set_mode([WIDTH, HEIGHT])

# Nastavení titulku okna
pygame.display.set_caption("Snowflake")

# Konstanty s n-ticemi představujícími základní barvy
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)


def apply_rule(rules, c):
    """Aplikace přepisovacího pravidla."""
    output = ""
    for rule, result in rules.items():
        if c == rule:
            return result
        else:
            output = c
    return output


def produce_control_string(axiom, rewrite_rules, n):
    """Výpočet řídicího řetězce."""
    s = axiom
    for i in range(n):
        tmp = ""
        for c in s:
            tmp += apply_rule(rewrite_rules, c)
        s = tmp
    return s


def draw_l_system(surface, color, control_string, step, angle_delta, start_x, start_y):
    """Vykreslení L-systému na obrazovku s využitím želví grafiky."""
    x = start_x
    y = start_y
    angle = 0

    # projít všemi příkazy z řídicího řetězce
    for command in control_string:
        if command == "F":
            xn = x + step * math.cos(angle)
            yn = y + step * math.sin(angle)
            draw.aaline(surface, color, (x, y), (xn, yn))
            x = xn
            y = yn
        elif command == "B":
            xn = x - step * math.cos(angle)
            yn = y - step * math.sin(angle)
            draw.aaline(surface, color, (x, y), (xn, yn))
            x = xn
            y = yn
        elif command == "+":
            angle -= angle_delta * math.pi / 180.0
        elif command == "-":
            angle += angle_delta * math.pi / 180.0


def draw_snowflake(surface, color):
    # krok želvy pro příkazy "F" a "B"
    step = 30

    # úhel otočení želvy pro příkazy "+" a "-"
    angle = 60

    # startovní symbol
    axiom = "F"

    # přepisovací pravidla
    rewrite_rules = {}
    rewrite_rules["F"] = "F+F--F+F"

    # počet aplikací přepisovacích pravidel
    iterations = 3

    # počáteční pozice želvy
    start_x = 0
    start_y = HEIGHT - 20

    # výpočet řídicího řetězce
    control_string = produce_control_string(axiom, rewrite_rules, iterations)
    print(control_string)

    # vykreslení L-systému
    draw_l_system(surface, color, control_string, step, angle, start_x, start_y)


# Vyplnění plochy okna černou barvou před začátkem vykreslování
display.fill(BLACK)

# Vykreslení fraktálu
draw_snowflake(display, WHITE)


def main():
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


if __name__ == "__main__":
    main()

# finito
