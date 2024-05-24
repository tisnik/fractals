"""Výpočet a vykreslení Lorenzova podivného atraktoru s efektem motýlích křídel."""

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
#
# Demonstrační příklad:
# - Lorenzův atraktor vykreslený v 3D prostoru

import matplotlib.pyplot as plt
import numpy as np


# funkce pro výpočet dalšího bodu Lorenzova atraktoru
def lorenz(x, y, z, s=10, r=28, b=2.667):
    """Výpočet dalšího bodu Lorenzova atraktoru."""
    x_dot = s * (y - x)
    y_dot = r * x - y - x * z
    z_dot = x * y - b * z
    return x_dot, y_dot, z_dot


# krok (změna času)
dt = 0.01

# celkový počet vypočtených bodů na Lorenzově atraktoru
n = 1000


def draw_lorenz_for_input_values(ax, dt, n, x0, y0, z0):
    """Vykreslení Lorenzova atraktoru."""
    # prozatím prázdné pole připravené pro výpočet
    x = np.zeros((n,))
    y = np.zeros((n,))
    z = np.zeros((n,))

    # počáteční hodnoty
    x[0], y[0], z[0] = (x0, y0, z0)

    # vlastní výpočet atraktoru
    for i in range(n - 1):
        x_dot, y_dot, z_dot = lorenz(x[i], y[i], z[i])
        x[i + 1] = x[i] + x_dot * dt
        y[i + 1] = y[i] + y_dot * dt
        z[i + 1] = z[i] + z_dot * dt

    # vykreslení grafu
    ax.plot(x.copy(), y.copy(), z.copy())


def draw_butterfly_effect(n):
    # konstrukce 3D grafu
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(projection="3d")
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)

    # změna velikosti komponent v grafu.
    plt.tight_layout()

    draw_lorenz_for_input_values(ax, dt, n, 0.0, 0.9, 1.05)
    draw_lorenz_for_input_values(ax, dt, n, 0.0, 0.8, 1.05)
    draw_lorenz_for_input_values(ax, dt, n, 0.0, 0.7, 1.05)

    # uložení grafu
    plt.savefig(f"butterfly_{n:04d}.png")

    # zobrazení grafu
    # plt.show()
    plt.close()


for n in np.linspace(50, 1500, 100):
    draw_butterfly_effect(int(n))
