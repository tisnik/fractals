"""Výpočet a vykreslení podivného atraktoru nazvaného Fractal Dream."""

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

# Dynamic system renderer

# import všech potřebných knihoven - Numpy, Matplotlibu a standardní
# matematické knihovny
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos


def dynamic(x, y, a, b):
    """Funkce pro výpočet dalšího bodu atraktoru."""
    x_dot = -sin(y + a*sin(b*y))
    y_dot = sin(x + a*sin(b*x))
    return x_dot, y_dot


# konstanta pro numerickou integraci
dt = 0.3

# parametry mřížky s počátečními hodnotami dynamického systému
max_x = 50
step_x = 5
max_y = 50
step_y = 5

# počet iterací pro zadané počáteční podmínky
maxiter = 1000

# počet vypočtených bodů na atraktoru
n = maxiter * max_x//step_x * max_y//step_y

# prozatím prázdné pole připravené pro výpočet
x = np.zeros((n,))
y = np.zeros((n,))

# počáteční hodnoty pro výpočet
# x[0], y[0] = (10, 10)

# parametry ovlivňující výpočet podivného atraktoru
A = -2.7
B = 2.8

i = 0
# vlastní výpočet atraktoru  pro různé počáteční podmínky
for x0 in range(0, max_x, step_x):
    for y0 in range(0, max_y, step_y):
        x[i], y[i] = (x0, y0)
        for r in range(1, maxiter):
            x_dot, y_dot = dynamic(x[i], y[i], A, B)
            x[i+1] = x[i] + dt*x_dot
            y[i+1] = y[i] + dt*y_dot
            i += 1

# vykreslení grafu
plt.plot(x, y, 'o', markersize=0.1)

# změna velikosti komponent v grafu
plt.tight_layout()

# uložení grafu pro jeho další zpracování
plt.savefig("dynamic.png")

# zobrazení grafu
plt.show()
