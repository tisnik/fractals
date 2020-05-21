
# coding: utf-8
# Pickover attractor
# In[42]:


# import všech potřebných knihoven - Numpy a Matplotlibu
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos


# In[85]:


# funkce pro výpočet dalšího bodu atraktoru
def dynamic(x, y, a, b):
    x_dot = -sin(y + a*sin(b*y))
    y_dot = sin(x + a*sin(b*x))
    return x_dot, y_dot


# In[95]:

dt = 0.3

# celkový počet vypočtených bodů na atraktoru
n = 100000

# prozatím prázdné pole připravené pro výpočet
x = np.zeros((n,))
y = np.zeros((n,))


# In[96]:


# počáteční hodnoty
# x[0], y[0] = (10, 10)

A = -2.7
B = 2.8

i = 0
# vlastní výpočet atraktoru
for x0 in range(0, 50, 5):
    for y0 in range(0, 50, 5):
        x[i], y[i] = (x0, y0)
        for r in range(1, 1000):
            x_dot, y_dot = dynamic(x[i], y[i], A, B)
            x[i+1] = x[i] + dt*x_dot
            y[i+1] = y[i] + dt*y_dot
            i += 1

# vykreslení grafu
plt.plot(x, y, 'o', markersize=0.1)

# zobrazení grafu
plt.tight_layout()
plt.show()

