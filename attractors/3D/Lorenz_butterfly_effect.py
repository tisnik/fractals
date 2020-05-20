# Jupyter Notebook
#
# Třicátý demonstrační příklad:
# - Lorenzův atraktor

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import math


# funkce pro výpočet dalšího bodu Lorenzova atraktoru
def lorenz(x, y, z, s=10, r=28, b=2.667):
    x_dot = s*(y - x)
    y_dot = r*x - y - x*z
    z_dot = x*y - b*z
    return x_dot, y_dot, z_dot


# krok (změna času)
dt = 0.01

# celkový počet vypočtených bodů na Lorenzově atraktoru
n = 1000


def draw_lorenz_for_input_values(ax, dt, n, x0, y0, z0):
    # prozatím prázdné pole připravené pro výpočet
    x = np.zeros((n,))
    y = np.zeros((n,))
    z = np.zeros((n,))

    # počáteční hodnoty
    x[0], y[0], z[0] = (x0, y0, z0)

    # vlastní výpočet atraktoru
    for i in range(n-1):
        x_dot, y_dot, z_dot = lorenz(x[i], y[i], z[i])
        x[i+1] = x[i] + x_dot * dt
        y[i+1] = y[i] + y_dot * dt
        z[i+1] = z[i] + z_dot * dt

    # vykreslení grafu
    ax.plot(x.copy(), y.copy(), z.copy())


fig = plt.figure()
ax = fig.gca(projection='3d')

draw_lorenz_for_input_values(ax, dt, n, 0.0, 0.9, 1.05)
draw_lorenz_for_input_values(ax, dt, n, 0.0, 0.8, 1.05)
draw_lorenz_for_input_values(ax, dt, n, 0.0, 0.7, 1.05)

# zobrazení grafu
plt.show()
