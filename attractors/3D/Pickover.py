"""Výpočet a vykreslení Pickoverova podivného atraktoru v 3D."""

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

# Pickover 3D attractor


# In[1]:


# import všech potřebných knihoven - Numpy a Matplotlibu
from math import cos, sin

import matplotlib.pyplot as plt
import numpy as np

# In[2]:


def pickover(x, y, z, a=2.24, b=0.43, c=-0.65, d=-2.43, e=1.0):
    """Výpočet dalšího bodu Pickoverova atraktoru."""
    x_dot = sin(a * y) - z * cos(b * x)
    y_dot = z * sin(c * x) - cos(d * y)
    z_dot = e * sin(x)
    return x_dot, y_dot, z_dot


# celkový počet vypočtených bodů na Lorenzově atraktoru
n = 100000

# prozatím prázdné pole připravené pro výpočet
x = np.zeros((n,))
y = np.zeros((n,))
z = np.zeros((n,))


# počáteční hodnoty
x[0], y[0], z[0] = (0.0, 0.0, 0.0)

# vlastní výpočet atraktoru
for i in range(n - 1):
    x_dot, y_dot, z_dot = pickover(x[i], y[i], z[i], 2.24, 0.43, -0.65, -2.43, 0.8)
    x[i + 1] = x_dot
    y[i + 1] = y_dot
    z[i + 1] = z_dot

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

# vykreslení grafu
ax.plot(x, y, z, "o", markersize=0.1)

# zobrazení grafu
plt.tight_layout()
# plt.show()

ch_3d = np.stack((x, y, z))
lim_xyz = [(np.min(ch_3d[ii]), np.max(ch_3d[ii])) for ii in range(3)]

fig2 = plt.figure("3D Coordinates")
plt.subplot(2, 2, 1)
plt.plot(y, x, "o", linewidth=0.75, markersize=0.1)
plt.grid()
plt.xlabel("X")
plt.ylabel("Y")
plt.xlim(lim_xyz[1])
plt.ylim(lim_xyz[0])

plt.subplot(2, 2, 2)
plt.plot(y, z, "o", linewidth=0.75, markersize=0.1)
plt.grid()
plt.xlabel("Z")
plt.ylabel("Y")
plt.xlim(lim_xyz[1])
plt.ylim(lim_xyz[2])

plt.subplot(2, 2, 3)
plt.plot(z, x, "o", linewidth=0.75, markersize=0.1)
plt.grid()
plt.xlabel("X")
plt.ylabel("Z")
plt.xlim(lim_xyz[2])
plt.ylim(lim_xyz[0])

ax = fig2.add_subplot(2, 2, 4, projection="3d")
ax.plot(x, y, z, "o", linewidth=0.7, markersize=0.1)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.tight_layout()

plt.tight_layout()
plt.show()
