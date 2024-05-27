# Vykreslení Lorenzova atraktoru s různými počátečními souřadnicemi x0 a y0

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
n = 500


def draw_lorenz_for_input_values(ax, dt, n, x0, y0, z0):
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
    ax.plot(y.copy(), z.copy())


# konstrukce 2D grafu
fig = plt.figure(figsize=(8, 6))
ax = fig.gca()


# vykreslení Lorenzova atraktoru s různými počátečními souřadnicemi x0 a y0
for y0 in np.arange(-1.5, 1.5, 0.5):
    for x0 in np.arange(-1.5, 1.5, 0.5):
        draw_lorenz_for_input_values(ax, dt, n, x0, y0, 1.05)

# změna velikosti komponent v grafu.
plt.tight_layout()

# uložení grafu
plt.savefig("variable_x0_y0_params.png")

# zobrazení grafu
plt.show()
