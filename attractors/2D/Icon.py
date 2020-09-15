"""Výpočet a vykreslení podivného atraktoru nazvaného Symmetric Icon."""

# MIT License
#
# Copyright (c) 2020 Pavel Tišnovský
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Pickover attractor

# Import všech potřebných knihoven - Numpy, Matplotlibu a standardní
# matematické knihovny, ze které se využijí jen některé vybrané funkce.
import matplotlib.pyplot as plt
import numpy as np


def icon(x, y, lambda_, alpha, beta, gamma, omega, degree):
    """Funkce pro výpočet dalšího bodu podivného atraktoru."""
    zzbar = x * x + y * y
    p = alpha * zzbar + lambda_
    zreal = x
    zimag = y
    for i in range(0, degree-2):
        za = zreal * x - zimag * y
        zb = zimag * x + zreal * y
        zreal = za
        zimag = zb
    zn = x * zreal - y * zimag
    p = p + beta * zn
    x_dot = p * x + gamma * zreal - omega * y
    y_dot = p * y - gamma * zimag + omega * x
    return x_dot, y_dot


def draw_icon(filename, lambda_, alfa, beta, gamma, omega, degree, color):
    # Celkový počet vypočtených bodů na atraktoru.
    n = 100000

    # Počet bodů ze začátku výpočtu, které se nevykreslí.
    settle_down_points = 10

    # Prozatím prázdné pole připravené pro uložení výsledků výpočtu.
    x = np.zeros((n,))
    y = np.zeros((n,))

    # Počáteční hodnoty pro výpočet.
    x[0], y[0] = (0.01, 0.01)

    # Vlastní výpočet podivného atraktoru.
    for i in range(n-1):
        x_dot, y_dot = icon(x[i], y[i],
                            LAMBDA, ALFA, BETA, GAMMA, OMEGA, DEGREE)
        x[i+1] = x_dot
        y[i+1] = y_dot

    # Změna velikosti komponent v grafu.
    plt.figure(figsize=(8, 8))

    # Vykreslení grafu.
    plt.plot(x[settle_down_points:], y[settle_down_points:], 'o',
             markersize=0.1, color=color)

    # Uložení grafu pro jeho další zpracování.
    plt.savefig(filename)

    # Zobrazení grafu.
    plt.show()


# První atraktor

# Parametry ovlivňující výpočet podivného atraktoru.
LAMBDA = -2.5
ALFA = 5
BETA = -1.9
GAMMA = 1
OMEGA = 0.188
DEGREE = 5

# Výsledek by měl vypadat následovně:
# ![icon_1.png](icon_1.png)
# (oproti originálu zmenšeno)
draw_icon("icon_1.png", LAMBDA, ALFA, BETA, GAMMA, OMEGA, DEGREE, 'blue')

# Druhý atraktor

LAMBDA = 1.56
ALFA = -1
BETA = 0.1
GAMMA = -0.82
OMEGA = 0.12
DEGREE = 3

# Výsledek by měl vypadat následovně:
# ![icon_2.png](icon_2.png)
# (oproti originálu zmenšeno)
draw_icon("icon_2.png", LAMBDA, ALFA, BETA, GAMMA, OMEGA, DEGREE, 'red')

# Třetí atraktor

LAMBDA = -1.806
ALFA = 1.806
BETA = 0
GAMMA = 1
OMEGA = 0
DEGREE = 5

# Výsledek by měl vypadat následovně:
# ![icon_3.png](icon_3.png)
# (oproti originálu zmenšeno)
draw_icon("icon_3.png", LAMBDA, ALFA, BETA, GAMMA, OMEGA, DEGREE, 'orange')


# Konec.
