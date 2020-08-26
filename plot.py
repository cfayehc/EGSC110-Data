# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 15:45:53 2020

@author: cfay
"""

import matplotlib.pyplot as pyplot
import numpy as np
figure = pyplot.figure()
axes = pyplot.axes()

x = np.linspace(0, 10, 1000)
axes.plot(x, x*x);

pyplot.show()