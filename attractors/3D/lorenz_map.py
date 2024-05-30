"""Map of Lorenz attractor."""

# MIT License
#
# Copyright (c) 2024 Pavel Tišnovský
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

# coding: utf-8

# # Mapa Lorenzova atraktoru


# import všech potřebných knihoven - Numpy a Matplotlibu
import matplotlib.pyplot as plt
import numpy as np


def lorenz(x, y, z, s=10, r=28, b=2.667):
    """Výpočet dalšího bodu Lorenzova atraktoru."""
    x_dot = s * (y - x)
    y_dot = r * x - y - x * z
    z_dot = x * y - b * z
    return x_dot, y_dot, z_dot


# krok (změna času)
dt = 0.005

# celkový počet vypočtených bodů na Lorenzově atraktoru
n = 20000

# prozatím prázdné pole připravené pro výpočet
x = np.zeros((n,))
y = np.zeros((n,))
z = np.zeros((n,))

# počáteční hodnoty
x[0], y[0], z[0] = (0.0, 0.5, 1.05)

# vlastní výpočet atraktoru
for i in range(n - 1):
    x_dot, y_dot, z_dot = lorenz(x[i], y[i], z[i])
    x[i + 1] = x[i] + x_dot * dt
    y[i + 1] = y[i] + y_dot * dt
    z[i + 1] = z[i] + z_dot * dt

WIDTH = 256
HEIGHT = 256
raster = np.zeros(shape=(HEIGHT, WIDTH, 3), dtype=np.uint8)


ax = 255.0 / (max(x) - min(x))
ox = min(x)
ay = 255.0 / (max(y) - min(y))
oy = min(y)
az = 255.0 / (max(z) - min(z))
oz = min(z)

# vytvoření mapy
for yi in range(HEIGHT):
    # počáteční hodnoty
    x[0], y[0], z[0] = (1.0, 0.5, 1.05)

    # vlastní výpočet atraktoru
    c = 2.0 + yi / 80.0
    for i in range(n - 1):
        x_dot, y_dot, z_dot = lorenz(x[i], y[i], z[i], 10, 28, c)
        x[i + 1] = x[i] + x_dot * dt
        y[i + 1] = y[i] + y_dot * dt
        z[i + 1] = z[i] + z_dot * dt

    for xi in range(WIDTH):
        raster[yi][xi][0] = (x[xi * 50] - ox) * ax
        raster[yi][xi][1] = (y[xi * 50] - oy) * ay
        raster[yi][xi][2] = (z[xi * 50] - oz) * az


plt.figure(1, figsize=(8, 6), dpi=100)
plt.imshow(raster)

# uložení grafu
plt.savefig("lorenz_map.png")

plt.show()
