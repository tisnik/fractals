
# coding: utf-8
# Fractal Dream attractor
# In[42]:


# import všech potřebných knihoven - Numpy a Matplotlibu
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, radians


# In[85]:


# funkce pro výpočet dalšího bodu atraktoru Fractal Dream
def fractal_dream(x, y, a, b, c, d):
    x_dot = sin(b * y) - c*sin(b * x)
    y_dot = sin(a * x) - d*sin(a * y)
    return x_dot, y_dot


# In[95]:


# celkový počet vypočtených bodů na atraktoru
n = 100000

# prozatím prázdné pole připravené pro výpočet
x = np.zeros((n,))
y = np.zeros((n,))


# In[96]:


# počáteční hodnoty
x[0], y[0] = (0.1, 0.0)

# vlastní výpočet atraktoru
for i in range(n-1):
    A = -0.97
    B =  2.88
    C =  0.77
    D =  0.74
    x_dot, y_dot = fractal_dream(x[i], y[i], A, B, C, D)
    x[i+1] = x_dot
    y[i+1] = y_dot

# vykreslení grafu
plt.plot(x[1000:], y[1000:], 'o', markersize=0.1)

# zobrazení grafu
plt.tight_layout()
plt.show()
