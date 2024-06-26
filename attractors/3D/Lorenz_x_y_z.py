"""Výpočet a vykreslení hodnot x, y, z Lorenzova podivného atraktoru."""

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

# Lorenz attractor

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
dt = 0.01

# celkový počet vypočtených bodů na Lorenzově atraktoru
n = 2000

# prozatím prázdné pole připravené pro výpočet
x = np.zeros((n,))
y = np.zeros((n,))
z = np.zeros((n,))

# počáteční hodnoty
x[0], y[0], z[0] = (0.0, 1.0, 1.05)

# vlastní výpočet bodů z nichž se postupně vytvoří Lorenzův systém
for i in range(n - 1):
    x_dot, y_dot, z_dot = lorenz(x[i], y[i], z[i])
    x[i + 1] = x[i] + x_dot * dt
    y[i + 1] = y[i] + y_dot * dt
    z[i + 1] = z[i] + z_dot * dt

# konstrukce 2D grafu s nastaveným rozlišením výsledného obrázku
fig = plt.figure(figsize=(8, 6))

# vykreslení grafu

ax = fig.add_subplot(3, 1, 1)
ax.plot(x)

ax = fig.add_subplot(3, 1, 2)
ax.plot(y)

ax = fig.add_subplot(3, 1, 3)
ax.plot(z)

# změna velikosti komponent v grafu.
plt.tight_layout()

# uložení grafu
plt.savefig("lorenz_x_y_z.png")

# zobrazení grafu
plt.show()
