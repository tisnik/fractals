"""Výpočet a vykreslení upraveného Lorenzova podivného atraktoru."""

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


# Please also see https://cdn.hipwallpaper.com/i/65/0/dP4ZTN.jpg

# In[7]:


# import všech potřebných knihoven - Numpy a Matplotlibu
import matplotlib.pyplot as plt
import numpy as np

# In[8]:


# funkce pro výpočet dalšího bodu Lorenzova mod2 atraktoru
def lorenz_mod2(x, y, z, alfa, beta, gamma, delta):
    """Výpočet dalšího bodu Lorenzove mod2 atraktoru."""
    x_dot = -alfa * x + y * y - z * z + alfa * gamma
    y_dot = x * (y - beta * z) + delta
    z_dot = -z + x * (beta * y + z)
    return x_dot, y_dot, z_dot


# In[9]:


# krok (změna času)
dt = 0.001

# celkový počet vypočtených bodů na Lorenzově atraktoru
n = 100000

# prozatím prázdné pole připravené pro výpočet
x = np.zeros((n,))
y = np.zeros((n,))
z = np.zeros((n,))


# In[10]:


# počáteční hodnoty
x[0], y[0], z[0] = (0.1, 0.1, 0)

# vlastní výpočet atraktoru
for i in range(n - 1):
    x_dot, y_dot, z_dot = lorenz_mod2(x[i], y[i], z[i], 0.9, 5.0, 9.9, 1.0)
    x[i + 1] = x[i] + x_dot * dt
    y[i + 1] = y[i] + y_dot * dt
    z[i + 1] = z[i] + z_dot * dt

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

# vykreslení grafu
ax.plot(x[50000:], y[50000:], z[50000:])

# zobrazení grafu
plt.tight_layout()
plt.show()


# In[11]:


ch_3d = np.stack((x, y, z))
lim_xyz = [(np.min(ch_3d[ii]), np.max(ch_3d[ii])) for ii in range(3)]

fig2 = plt.figure("3D Coordinates")
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

plt.tight_layout()
plt.show()
