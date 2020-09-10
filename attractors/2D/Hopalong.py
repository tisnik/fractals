"""Výpočet a vykreslení podivného atraktoru nazvaného Hopalong."""

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

# Hopalong attractor

# Import všech potřebných knihoven - Numpy, Matplotlibu a standardní
# matematické knihovny, ze které se využijí jen některé vybrané funkce.
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, sqrt


def sign(x):
    """Výpočet znaménka ze zadané hodnoty. Výsledkem je hodnota 1 nebo 0."""
    if x > 0:
        # kladný vstup
        return 1
    # záporný vstup
    return 0


def sign2(x):
    """Výpočet znaménka ze zadané hodnoty. Výsledkem je hodnota 1 nebo -1."""
    if x > 0:
        # kladný vstup
        return 1
    # záporný vstup
    return -1


def hopalong(x, y, a, b, c):
    """Funkce pro výpočet dalšího bodu podivného atraktoru Hopalong."""
    x_dot = y - sign(x)*sqrt(abs(b*x-c))
    y_dot = a - x
    return x_dot, y_dot


# Celkový počet vypočtených bodů na atraktoru.
n = 200000

# Počet bodů ze začátku výpočtu, které se nevykreslí.
settle_down_points = 10

# Prozatím prázdné pole připravené pro uložení výsledků výpočtu.
x = np.zeros((n,))
y = np.zeros((n,))

# Počáteční hodnoty pro výpočet.
x[0], y[0] = (0.0, 0.0)

# Parametry ovlivňující výpočet podivného atraktoru.
A = 3.1
B = 1.8
C = -0.9

# Vlastní výpočet podivného atraktoru.
for i in range(n-1):
    x_dot, y_dot = hopalong(x[i], y[i], A, B, C)
    x[i+1] = x_dot
    y[i+1] = y_dot

# Vykreslení grafu.
plt.plot(x[settle_down_points:], y[settle_down_points:], 'o', markersize=0.1)

# Změna velikosti komponent v grafu.
plt.tight_layout()

# Uložení grafu pro jeho další zpracování.
plt.savefig("hopalong.png")

# Výsledek by měl vypadat následovně:
# ![hopalong.png](hopalong.png)
# (oproti originálu zmenšeno)

# Zobrazení grafu.
plt.show()

# Konec.
