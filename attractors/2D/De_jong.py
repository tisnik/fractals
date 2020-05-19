
# coding: utf-8
# De Jong attractor
# In[42]:


# import všech potřebných knihoven - Numpy a Matplotlibu
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, radians


# In[85]:


# funkce pro výpočet dalšího bodu De Jongova atraktoru
def de_jong(x, y, a, b, c, d):
    x_dot = sin(a * y) - cos(b * x)
    y_dot = sin(c * x) - cos(d * y)
    return x_dot, y_dot


# In[95]:


# celkový počet vypočtených bodů na atraktoru
n = 500000

# prozatím prázdné pole připravené pro výpočet
x = np.zeros((n,))
y = np.zeros((n,))


# In[96]:


# počáteční hodnoty
x[0], y[0] = (0.0, 0.0)

# vlastní výpočet atraktoru
for i in range(n-1):
    A = -2.7
    B = -0.09
    C = -0.86
    D = -2.20
    x_dot, y_dot = de_jong(x[i], y[i], A, B, C, D)
    x[i+1] = x_dot
    y[i+1] = y_dot

# vykreslení grafu
plt.plot(x[1000:], y[1000:], 'o', markersize=0.1)

# zobrazení grafu
plt.tight_layout()
plt.show()

# vlastní výpočet atraktoru
for i in range(n-1):
    A = 1.641
    B = 1.902
    C = 0.316
    D= 1.525
    x_dot, y_dot = de_jong(x[i], y[i], A, B, C, D)
    x[i+1] = x_dot
    y[i+1] = y_dot

# vykreslení grafu
plt.plot(x[1000:], y[1000:], 'o', markersize=0.1)

# zobrazení grafu
plt.tight_layout()
plt.show()

