# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 11:23:18 2021

@author: ruadh
"""

import matplotlib.pyplot as plt

x11 = [25000, 25000, 24800]
x21 = [35000, 20600, 20000]
x12 = [25000, 25000, 25200]
x22 = [15000, 29400, 30000]

TPC = [310689, 309375, 309311]
SSPV = [86492, 85027.52, 84946.16]

x_lab = ['W1 = 0.4 \nW2 = 0.6', 'W1 = 0.5 \nW2 = 0.5', 'W1 = 0.6 \nW2 = 0.4']


plt.plot(x_lab, x11, 'bs-', x_lab, x21, 'rs-')
plt.xlabel('(a)')
plt.grid(axis = 'y')
plt.show()

plt.plot(x_lab, x12, 'bs-', x_lab, x22, 'rs-')
plt.xlabel('(b)')
plt.grid(axis = 'y')
plt.show()

plt.plot(x_lab, TPC, 'bs-')
plt.xlabel('(c)')
plt.grid(axis = 'y')
plt.show()

plt.plot(x_lab, SSPV, 'bs-')
plt.xlabel('(d)')
plt.grid(axis = 'y')
plt.show()