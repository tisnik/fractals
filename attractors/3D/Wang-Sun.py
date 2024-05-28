"""Výpočet a vykreslení Wang-Sunova podivného atraktoru."""

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

# # The Wang - Sun attractor
# Please also see https://hipwallpaper.com/view/9W3CM8


# import všech potřebných knihoven - Numpy a Matplotlibu
import matplotlib.pyplot as plt
import numpy as np


def wang_sun(x, y, z, alfa, beta, gamma, delta, epsilon, zeta):
    """Výpočet dalšího bodu Wang-Sunova atraktoru."""
    x_dot = x * alfa + gamma * y * z
    y_dot = x * beta + y * delta - x * z
    z_dot = z * epsilon + zeta * x * y
    return x_dot, y_dot, z_dot


# krok (změna času)
dt = 0.001

# celkový počet vypočtených bodů na Lorenzově atraktoru
n = 1000000

# prozatím prázdné pole připravené pro výpočet
x = np.zeros((n,))
y = np.zeros((n,))
z = np.zeros((n,))

# počáteční hodnoty
x[0], y[0], z[0] = (1.05, 1.1, 1.5)

# vlastní výpočet atraktoru
for i in range(n - 1):
    x_dot, y_dot, z_dot = wang_sun(x[i], y[i], z[i], 0.2, -0.01, 1.0, -0.4, -1.0, -1.0)
    x[i + 1] = x[i] + x_dot * dt
    y[i + 1] = y[i] + y_dot * dt
    z[i + 1] = z[i] + z_dot * dt

# konstrukce 3D grafu
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(projection="3d")

# změna velikosti komponent v grafu.
plt.tight_layout()

# vykreslení grafu
ax.plot(x, y, z)

# uložení grafu
plt.savefig("wang_sun_1.png")

# zobrazení grafu
plt.show()

# grafy s více pohledy na atraktor
ch_3d = np.stack((x, y, z))
lim_xyz = [(np.min(ch_3d[ii]), np.max(ch_3d[ii])) for ii in range(3)]

fig2 = plt.figure("3D Coordinates", figsize=(8, 6))
plt.subplot(2, 2, 1)
plt.plot(y, x, linewidth=0.75)
plt.grid()
plt.xlabel("X")
plt.ylabel("Y")
plt.xlim(lim_xyz[1])
plt.ylim(lim_xyz[0])

plt.subplot(2, 2, 2)
plt.plot(y, z, linewidth=0.75)
plt.grid()
plt.xlabel("Z")
plt.ylabel("Y")
plt.xlim(lim_xyz[1])
plt.ylim(lim_xyz[2])

plt.subplot(2, 2, 3)
plt.plot(z, x, linewidth=0.75)
plt.grid()
plt.xlabel("X")
plt.ylabel("Z")
plt.xlim(lim_xyz[2])
plt.ylim(lim_xyz[0])

ax = fig2.add_subplot(2, 2, 4, projection="3d")
ax.plot(x, y, z, linewidth=0.7)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.tight_layout()

# uložení grafu
plt.savefig("wang_sun_2.png")

# zobrazení grafu
plt.show()
