
# coding: utf-8
# Kam Torus attractor
# In[42]:


# import všech potřebných knihoven - Numpy a Matplotlibu
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, radians


# In[85]:


def frange(start, stop, step):
    x = start
    while x < stop:
        yield x
        x += step

# počáteční hodnoty
orbit_start = 0.0
orbit_end = 1.5
orbit_step = 0.03
points_per_orbit = 2000

a = 1.3

def kam_torus(orbit_start, orbit_end, orbit_step, points_per_orbit, a):
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
                return x,y
    return x, y

x, y = kam_torus(orbit_start, orbit_end, orbit_step, points_per_orbit, a)

# vykreslení grafu
plt.plot(x, y, 'o', markersize=0.1)

# zobrazení grafu
plt.tight_layout()
plt.show()
