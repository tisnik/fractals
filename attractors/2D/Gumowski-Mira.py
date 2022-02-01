"""Výpočet a vykreslení podivného atraktoru vytvořeného I.Gumowskim a L.Mirou."""

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

# Gumowki-Mira attractor

# Import všech potřebných knihoven - Numpy, Matplotlibu a standardní
# matematické knihovny, ze které se využijí jen některé vybrané funkce.
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, sqrt


def Gumowski(x, mu):
    """Gumovského funkce."""
    g = x * mu + 2 * x * x * (1 - mu) / (1 + x * x)
    return g


def gumowski_mira(x, y, a, b, mu):
    """Funkce pro výpočet dalšího bodu podivného atraktoru Gumowski-Mira."""
    x_dot = a * y * (1 - b * y * y) + y + Gumowski(x, mu)
    y_dot = -x + Gumowski(x_dot, mu)
    return x_dot, y_dot


# Celkový počet vypočtených bodů na atraktoru.
n = 1000000

# Počet bodů ze začátku výpočtu, které se nevykreslí.
settle_down_points = 10

# Prozatím prázdné pole připravené pro uložení výsledků výpočtu.
x = np.zeros((n,))
y = np.zeros((n,))

# Počáteční hodnoty pro výpočet.
x[0], y[0] = (0, 0.1)

# Parametry ovlivňující výpočet podivného atraktoru.
A = 0.01
B = 0.5
mu = -0.8

# Vlastní výpočet podivného atraktoru.
for i in range(n - 1):
    x_dot, y_dot = gumowski_mira(x[i], y[i], A, B, mu)
    x[i + 1] = x_dot
    y[i + 1] = y_dot

# Vykreslení grafu.
plt.plot(x[settle_down_points:], y[settle_down_points:], "o", markersize=0.1)

# Změna velikosti komponent v grafu.
plt.tight_layout()

# Uložení grafu pro jeho další zpracování.
plt.savefig("gumowski_mira_1.png")

# Výsledek by měl vypadat následovně:
# ![gumowski_mira_1.png](gumowski_mira_1.png)
# (oproti originálu zmenšeno)

# Zobrazení grafu.
plt.show()

# Druhý atraktor

# Parametry ovlivňující výpočet podivného atraktoru.
A = 0.01
B = 0.15
mu = -0.9

# Vlastní výpočet druhého podivného atraktoru.
for i in range(n - 1):
    x_dot, y_dot = gumowski_mira(x[i], y[i], A, B, mu)
    x[i + 1] = x_dot
    y[i + 1] = y_dot

# Vykreslení grafu.
plt.plot(
    x[settle_down_points:], y[settle_down_points:], "o", markersize=0.1, color="red"
)

# Změna velikosti komponent v grafu.
plt.tight_layout()

# Uložení grafu pro jeho další zpracování.
plt.savefig("gumowski_mira_2.png")

# Výsledek by měl vypadat následovně:
# ![gumowski_mira_2.png](gumowski_mira_2.png)
# (oproti originálu zmenšeno)

# Zobrazení grafu.
plt.show()

# Konec.
