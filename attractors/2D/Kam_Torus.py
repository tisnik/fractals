"""Výpočet a vykreslení podivného atraktoru nazvaného Kam torus."""

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

# Kam torus attractor

# import všech potřebných knihoven - Numpy, Matplotlibu a standardní
# matematické knihovny
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos


def frange(start, stop, step):
    """Generátor sekvence hodnot s plovoucí řádovou čárkou."""
    x = start
    while x < stop:
        yield x
        x += step


# počáteční hodnoty
orbit_start = 0.0
orbit_end = 1.5
orbit_step = 0.03
points_per_orbit = 2000

# parametry pro výpočet atraktoru
a = 1.3


def kam_torus(orbit_start, orbit_end, orbit_step, points_per_orbit, a):
    """Výpočet atraktoru."""
    # celkový počet vypočtených bodů na atraktoru
    n = 100000

    # prozatím prázdné pole připravené pro výpočet
    x = np.zeros((n,))
    y = np.zeros((n,))

    # vlastní výpočet atraktoru
    i = 0
    for orbit in frange(orbit_start, orbit_end, orbit_step):
        x[i] = orbit/3.0
        y[i] = orbit/3.0
        i += 1
        if i >= n:
            return x, y
        for p in range(1, points_per_orbit):
            x[i] = x[i-1]*cos(a) + (x[i-1]*x[i-1]-y[i-1])*sin(a)
            y[i] = x[i-1]*sin(a) - (x[i-1]*x[i-1]-y[i-1])*cos(a)
            i += 1
            if i >= n:
                return x, y
    return x, y


# výpočet
x, y = kam_torus(orbit_start, orbit_end, orbit_step, points_per_orbit, a)

# vykreslení grafu
plt.plot(x, y, 'o', markersize=0.1)

# změna velikosti komponent v grafu
plt.tight_layout()

# uložení grafu pro jeho další zpracování
plt.savefig("kam_torus.png")

# zobrazení grafu
plt.show()
