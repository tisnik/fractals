"""Výpočet a vykreslení podivného atraktoru navrženého Johny Svenssonem."""

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

# Quadruptwo attractor

# Import všech potřebných knihoven - Numpy, Matplotlibu a standardní
# matematické knihovny, ze které se využijí jen některé vybrané funkce.
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos


def svensson(x, y, a, b, c, d):
    """Funkce pro výpočet dalšího bodu podivného atraktoru."""
    x_dot = d * sin(x * a) - sin(y * b)
    y_dot = c * cos(x * a) + cos(y * b)
    return x_dot, y_dot


# Celkový počet vypočtených bodů na atraktoru.
n = 400000

# Počet bodů ze začátku výpočtu, které se nevykreslí.
settle_down_points = 1

# Prozatím prázdné pole připravené pro uložení výsledků výpočtu.
x = np.zeros((n,))
y = np.zeros((n,))

# Počáteční hodnoty pro výpočet.
x[0], y[0] = (0.0, 0.0)

# Parametry ovlivňující výpočet podivného atraktoru.
A = -2.337
B = -2.337
C = 0.533
D = 1.378

# Vlastní výpočet podivného atraktoru.
for i in range(n - 1):
    x_dot, y_dot = svensson(x[i], y[i], A, B, C, D)
    x[i + 1] = x_dot
    y[i + 1] = y_dot

# Vykreslení grafu.
plt.plot(x[settle_down_points:], y[settle_down_points:], "o", markersize=0.05)

# Změna velikosti komponent v grafu.
plt.tight_layout()

# Uložení grafu pro jeho další zpracování.
plt.savefig("svensson_1.png")

# Výsledek by měl vypadat následovně:
# ![svensson_1.png](svensson_1.png)
# (oproti originálu zmenšeno)

# Zobrazení grafu.
plt.show()

# Druhý atraktor

# Parametry ovlivňující výpočet podivného atraktoru.
A = 1.40
B = 1.56
C = 1.40
D = -6.56

# Vlastní výpočet podivného atraktoru.
for i in range(n - 1):
    x_dot, y_dot = svensson(x[i], y[i], A, B, C, D)
    x[i + 1] = x_dot
    y[i + 1] = y_dot

# Vykreslení grafu.
plt.plot(
    x[settle_down_points:], y[settle_down_points:], "o", markersize=0.05, color="red"
)

# Změna velikosti komponent v grafu.
plt.tight_layout()

# Uložení grafu pro jeho další zpracování.
plt.savefig("svensson_2.png")

# Výsledek by měl vypadat následovně:
# ![svensson_2.png](svensson_2.png)
# (oproti originálu zmenšeno)

# Zobrazení grafu.
plt.show()

# Konec.
