# Jupyter Notebook
#
# Třicátý demonstrační příklad:
# - Lorenzův atraktor

import matplotlib.pyplot as plt
import numpy as np


# funkce pro výpočet dalšího bodu Lorenzova atraktoru
def lorenz(x, y, z, s=10, r=28, b=2.667):
    x_dot = s * (y - x)
    y_dot = r * x - y - x * z
    z_dot = x * y - b * z
    return x_dot, y_dot, z_dot


# krok (změna času)
dt = 0.01

# celkový počet vypočtených bodů na Lorenzově atraktoru
n = 1000


def draw_lorenz_for_input_values(ax, dt, n, x0, y0, z0, s, r, b):
    # prozatím prázdné pole připravené pro výpočet
    x = np.zeros((n,))
    y = np.zeros((n,))
    z = np.zeros((n,))

    # počáteční hodnoty
    x[0], y[0], z[0] = (x0, y0, z0)

    # vlastní výpočet atraktoru
    for i in range(n - 1):
        x_dot, y_dot, z_dot = lorenz(x[i], y[i], z[i], s, r, b)
        x[i + 1] = x[i] + x_dot * dt
        y[i + 1] = y[i] + y_dot * dt
        z[i + 1] = z[i] + z_dot * dt

    # vykreslení grafu
    ax.plot(y.copy(), z.copy())


# konstrukce 2D grafu
fig = plt.figure(figsize=(8, 6))

b = 2.667

# vykreslení Lorenzova atraktoru s různými parametry s a r
for si in range(5):
    for ri in range(5):
        ax = fig.add_subplot(5, 5, si + 1 + ri * 5)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        draw_lorenz_for_input_values(ax, dt, n, 0.0, 1.0, 1.05, si * 2.0 + 1.0, 4.0 + ri * 4, b)

# změna velikosti komponent v grafu.
plt.tight_layout()

# uložení grafu
plt.savefig("variable_s_r_params_multiplot.png")

# zobrazení grafu
plt.show()
