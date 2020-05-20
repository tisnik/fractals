
# coding: utf-8
# Hopalong attractor
# In[42]:


# import všech potřebných knihoven - Numpy a Matplotlibu
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, sqrt, radians


# In[85]:


def sign(x):
    if x>0:
        return 1
    return 0


# funkce pro výpočet dalšího bodu Hopalongova atraktoru
def hopalong(x, y, a, b, c):
    x_dot = y - sign(x)*sqrt(abs(b*x-c))
    y_dot = a - x
    return x_dot, y_dot


# In[95]:


# celkový počet vypočtených bodů na atraktoru
n = 200000

# prozatím prázdné pole připravené pro výpočet
x = np.zeros((n,))
y = np.zeros((n,))


# In[96]:


# počáteční hodnoty
x[0], y[0] = (0.0, 0.0)

# vlastní výpočet atraktoru
for i in range(n-1):
    A = 3.1
    B = 1.8
    C = -0.9
    x_dot, y_dot = hopalong(x[i], y[i], A, B, C)
    x[i+1] = x_dot
    y[i+1] = y_dot

# vykreslení grafu
plt.plot(x, y, 'o', markersize=0.1)

# zobrazení grafu
plt.tight_layout()
plt.show()

