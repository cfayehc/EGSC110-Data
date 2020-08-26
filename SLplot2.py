# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 11:41:19 2020

@author: cfay
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.optimize import curve_fit
from pylab import rcParams
rcParams['figure.figsize'] = 20,10

plt.close('all')

# read the data
with open('SL.csv','r') as f:
    reader=csv.reader(f,delimiter=',')
    next(reader, None)
    data=np.array([tuple(row[0:]+row[:1]) for row in reader],dtype=None)

# print(mc.report_memory())   




# font style
labelfont = {
        'family' : 'sans-serif',  # (cursive, fantasy, monospace, serif)
        'color'  : 'black',       # html hex or colour name
        'weight' : 'normal',      # (normal, bold, bolder, lighter)
        'size'   : 36,            # default value:12
        }

titlefont = {
        'family' : 'serif',
        'color'  : 'black',
        'weight' : 'bold',
        'size'   : 40,
        }

# delete garbage
#data = np.delete(data, 0, 0)
#data = np.delete(data, 0, 0)

# title and labels
plt.title('SemiLog Plot', fontdict=titlefont) 
plt.xlabel('x', fontdict=labelfont)
plt.ylabel('y', fontdict=labelfont)
plt.xscale('log')
plt.minorticks_on()
plt.grid(b=True, which='major', color='0.65', linestyle='-')
plt.grid(b=True, which='minor', color='0.65', linestyle='--')
# adjust fontsize of ticks
plt.tick_params(axis='both', which='major', labelsize=30)
plt.tick_params(axis='both', which='minor', labelsize=30)

# return data as float
data = data.astype(float)

# just for regression
xdata = data[:,1]
ydata = data[:,2]

# logarithmic function
def func(x, p1,p2):
  return p1*np.log(x)+p2

popt, pcov = curve_fit(func, xdata, ydata,p0=(5,10.2))

# curve params
p1 = popt[0]
p2 = popt[1]

# plot curve
curvex=np.linspace(5,1500,1000)
curvey=func(curvex,p1,p2)
plt.plot(curvex,curvey,'r', linewidth=5)
plt.text(5,8,'y =%0.2f log x + %0.2f' %(p1, p2),fontsize=36)

# plot data
plt.plot(data[:,1],data[:,2],'x',label = 'Xsaved')

plt.show()