"""Fresnel fractal generator."""

from math import cos, sin

import matplotlib.pyplot as plt
import numpy as np

# Celkový počet vypočtených bodů
n = 10000

# Prozatím prázdná pole připravená pro uložení výsledků výpočtu.
xa = np.zeros((n,))
ya = np.zeros((n,))


x = 0.0
y = 0.0
f = 0.0

for i in range(n):
    f += 0.05
    x += cos(f * f)
    y += sin(f * f)
    xa[i] = x
    ya[i] = y

# Vykreslení grafu
plt.plot(xa, ya, "b")

# Změna velikosti komponent v grafu.
# plt.tight_layout()

plt.show()

# Uložení grafu pro jeho další zpracování.
plt.savefig("fresnel.png")
