
# coding: utf-8
# Pickover attractor
# In[42]:


# import všech potřebných knihoven - Numpy a Matplotlibu
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos


# In[85]:


# funkce pro výpočet dalšího bodu Pickoverova atraktoru
def pickover(x, y, a, b, c, d):
    x_dot = sin(a * y) + c * cos(a * x)
    y_dot = sin(b * x) + d * cos(b * y)
    return x_dot, y_dot


# In[95]:


# celkový počet vypočtených bodů na atraktoru
n = 100000

# prozatím prázdné pole připravené pro výpočet
x = np.zeros((n,))
y = np.zeros((n,))


# In[96]:


# počáteční hodnoty
x[0], y[0] = (0.1, 0.1)

# vlastní výpočet atraktoru
for i in range(n-1):
    A = -1.7
    B = 1.8
    C = -0.9
    D = -0.4
    x_dot, y_dot = pickover(x[i], y[i], A, B, C, D)
    x[i+1] = x_dot
    y[i+1] = y_dot

# vykreslení grafu
plt.plot(x, y, 'o', markersize=0.1)

# zobrazení grafu
plt.tight_layout()
plt.show()

