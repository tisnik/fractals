
# coding: utf-8

# # Pickover 3D attractor

# In[1]:


# import všech potřebných knihoven - Numpy a Matplotlibu
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos


# In[2]:


def pickover(x, y, z, a=2.24, b=0.43, c=-0.65, d=-2.43, e=1.0):
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
for i in range(n-1):
    x_dot, y_dot, z_dot = pickover(x[i], y[i], z[i], 2.24, 0.43, -0.65, -2.43, 0.8)
    x[i+1] = x_dot
    y[i+1] = y_dot
    z[i+1] = z_dot

fig = plt.figure()
ax = fig.gca(projection='3d')

# vykreslení grafu
ax.plot(x, y, z, 'o', markersize=0.1)

# zobrazení grafu
plt.tight_layout()
#plt.show()

ch_3d = np.stack((x, y, z))
lim_xyz = [(np.min(ch_3d[ii]), np.max(ch_3d[ii])) for ii in range(3)]

fig2 = plt.figure('3D Coordinates')
plt.subplot(2, 2, 1)
plt.plot(y, x, 'o', linewidth=0.75, markersize=0.1)
plt.grid()
plt.xlabel('X')
plt.ylabel('Y')
plt.xlim(lim_xyz[1])
plt.ylim(lim_xyz[0])

plt.subplot(2, 2, 2)
plt.plot(y, z, 'o', linewidth=0.75, markersize=0.1)
plt.grid()
plt.xlabel('Z')
plt.ylabel('Y')
plt.xlim(lim_xyz[1])
plt.ylim(lim_xyz[2])

plt.subplot(2, 2, 3)
plt.plot(z, x, 'o', linewidth=0.75, markersize=0.1)
plt.grid()
plt.xlabel('X')
plt.ylabel('Z')
plt.xlim(lim_xyz[2])
plt.ylim(lim_xyz[0])

ax = fig2.add_subplot(2, 2, 4, projection='3d')
ax.plot(x, y, z, 'o', linewidth=0.7, markersize=0.1)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.tight_layout()

plt.tight_layout()
plt.show()

