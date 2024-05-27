# Vykreslení Lorenzova atraktoru s různými počátečními souřadnicemi x0 a y0

import matplotlib.pyplot as plt
import numpy as np


def lorenz(x, y, z, s=10, r=2.0, b=2.667):
    """Výpočet dalšího bodu Lorenzova atraktoru."""
    x_dot = s * (y - x)
    y_dot = r * x - y - x * z
    z_dot = x * y - b * z
    return x_dot, y_dot, z_dot


# krok (změna času)
dt = 0.01

# celkový počet vypočtených bodů na Lorenzově atraktoru
n = 250


def draw_lorenz_for_input_values(ax, dt, n, x0, y0, z0, r, skip):
    # prozatím prázdné pole připravené pro výpočet
    x = np.zeros((n,))
    y = np.zeros((n,))
    z = np.zeros((n,))

    # počáteční hodnoty
    x[0], y[0], z[0] = (x0, y0, z0)

    # vlastní výpočet atraktoru
    for i in range(n - 1):
        x_dot, y_dot, z_dot = lorenz(x[i], y[i], z[i], r=r)
        x[i + 1] = x[i] + x_dot * dt
        y[i + 1] = y[i] + y_dot * dt
        z[i + 1] = z[i] + z_dot * dt

    # vykreslení grafu
    ax.plot(y.copy()[skip:skip+20], z.copy()[skip:skip+20])


def anim_attractor_for_r(r):
    # konstrukce 2D grafu
    for skip in range(0, n-50):
        fig = plt.figure(figsize=(4, 3))
        ax = fig.gca()
        ax.set_xlim(-20, 20)
        ax.set_ylim(-10, 30)


        # vykreslení Lorenzova atraktoru s různými počátečními souřadnicemi x0 a y0
        x0 = 0.0
        for y0 in np.linspace(-15.0, 15.0, 7):
            for z0 in np.linspace(-10.0, 20.0, 7):
                draw_lorenz_for_input_values(ax, dt, n, x0, y0, z0, r, skip)

        plt.grid()
        # změna velikosti komponent v grafu.
        plt.tight_layout()

        # uložení grafu
        plt.savefig(f"variable_x0_y0_params_r_{r:04.1f}_{skip:03d}.png")

        # zobrazení grafu
        #plt.show()
        plt.close()


anim_attractor_for_r(1.0)
anim_attractor_for_r(2.0)
anim_attractor_for_r(5.0)
anim_attractor_for_r(14.0)
