"""Výpočet a vykreslení podivného atraktoru vytvořeného Jasonem Rampem 1."""

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

# Jason Rampe attractor #1
# https://softologyblog.wordpress.com/2017/03/04/2d-strange-attractors/

# Import všech potřebných knihoven - Numpy, Matplotlibu a standardní
# matematické knihovny, ze které se využijí jen některé vybrané funkce.
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos


def rason_rampe_1(x, y, a, b, c, d):
    """Funkce pro výpočet dalšího bodu podivného atraktoru."""
    x_dot = cos(b * y) + c * sin(b * x)
    y_dot = cos(a * x) + d * sin(a * y)
    return x_dot, y_dot


# Celkový počet vypočtených bodů na atraktoru.
n = 400000

# Počet bodů ze začátku výpočtu, které se nevykreslí.
settle_down_points = 1

# Prozatím prázdné pole připravené pro uložení výsledků výpočtu.
x = np.zeros((n,))
y = np.zeros((n,))

# Počáteční hodnoty pro výpočet.
x[0], y[0] = (0.1, 0.1)

# Parametry ovlivňující výpočet podivného atraktoru.
A = -2.7918
B = 2.1196
C = 1.0284
D = 0.1384

# Vlastní výpočet podivného atraktoru.
for i in range(n - 1):
    x_dot, y_dot = rason_rampe_1(x[i], y[i], A, B, C, D)
    x[i + 1] = x_dot
    y[i + 1] = y_dot

# Vykreslení grafu.
plt.plot(x[settle_down_points:], y[settle_down_points:], "o", markersize=0.03)

# Změna velikosti komponent v grafu.
plt.tight_layout()

# Uložení grafu pro jeho další zpracování.
plt.savefig("rason_rampe_1.png")

# Výsledek by měl vypadat následovně:
# ![rason_rampe_1.png](rason_rampe_1.png)
# (oproti originálu zmenšeno)

# Zobrazení grafu.
plt.show()

# Konec.
