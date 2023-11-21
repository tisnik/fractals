"""Výpočet a vykreslení Wan-Sunova podivného atraktoru."""

# coding: utf-8

# # The Wang - Sun attractor
# Please also see https://hipwallpaper.com/view/9W3CM8

# In[1]:


# import všech potřebných knihoven - Numpy a Matplotlibu
import matplotlib.pyplot as plt
import numpy as np


# In[2]:


# funkce pro výpočet dalšího bodu Wang-Sunova atraktoru
def wang_sun(x, y, z, alfa, beta, gamma, delta, epsilon, zeta):
    """Výpočet dalšího bodu Wang-Sunova atraktoru."""
    x_dot = x * alfa + gamma * y * z
    y_dot = x * beta + y * delta - x * z
    z_dot = z * epsilon + zeta * x * y
    return x_dot, y_dot, z_dot


# In[14]:


# krok (změna času)
dt = 0.001

# celkový počet vypočtených bodů na Lorenzově atraktoru
n = 1000000

# prozatím prázdné pole připravené pro výpočet
x = np.zeros((n,))
y = np.zeros((n,))
z = np.zeros((n,))


# In[15]:


# počáteční hodnoty
x[0], y[0], z[0] = (1.05, 1.1, 1.5)

# vlastní výpočet atraktoru
for i in range(n - 1):
    x_dot, y_dot, z_dot = wang_sun(x[i], y[i], z[i], 0.2, -0.01, 1.0, -0.4, -1.0, -1.0)
    x[i + 1] = x[i] + x_dot * dt
    y[i + 1] = y[i] + y_dot * dt
    z[i + 1] = z[i] + z_dot * dt

fig = plt.figure()
ax = fig.gca(projection="3d")

# vykreslení grafu
ax.plot(x, y, z)

# zobrazení grafu
plt.tight_layout()
plt.show()


# In[16]:


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
