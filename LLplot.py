# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 15:45:53 2020

@author: cfay
"""

#function definition

def trendline1(xd, yd, order=1, c='r', alpha=1, Rval=False):
    """Make a line of best fit"""

    #Calculate trendline
    coeffs = np.polyfit(xd, yd, order)

    intercept = coeffs[-1]
    slope = coeffs[-2]
    power = coeffs[0] if order == 2 else 0

    minxd = np.min(xd)
    maxxd = np.max(xd)

    xl = np.array([minxd, maxxd])
    yl = power * xl ** 2 + slope * xl + intercept

    #Plot trendline
    plt.plot(xl, yl, c, alpha=alpha)
    plt.text(0.22 * maxxd + 0.2 * minxd, 0.8 * np.max(yd) + 0.2 * np.min(yd),
                 '$y = %0.3f$ x + %0.3f' %(slope,intercept))

    #Calculate R Squared
    p = np.poly1d(coeffs)

    ybar = np.sum(yd) / len(yd)
    ssreg = np.sum((p(xd) - ybar) ** 2)
    sstot = np.sum((yd - ybar) ** 2)
    Rsqr = ssreg / sstot

    if not Rval:
        #Plot R^2 value
        plt.text(0.8 * maxxd + 0.2 * minxd, 0.8 * np.max(yd) + 0.2 * np.min(yd),
                 '$R^2 = %0.2f$' % Rsqr)
    else:
        #Return the R^2 value:
        return Rsqr
        
# Function to calculate the exponential with constants a and b
def exponential(x, p1, p2):
    return p1*np.power(x, p2)        
        
def trendline(xd, yd, order=1, c='r', alpha=1, Rval=False):        
    
# just for regression
#xdata = data[:,1]
#ydata = data[:,2]

# Import curve fitting package from scipy
    from scipy.optimize import curve_fit

    popt, pcov = curve_fit(exponential, xd, yd, p0=(10,2), bounds=(-np.inf, np.inf))

# curve params
    #p1 = 10
    #p2 = 2
    p1 = popt[0]
    p2 = popt[1]


# plot curve
    minxd = np.min(xd)
    maxxd = np.max(xd)

    curvex=np.linspace(.3,200)
    curvey=exponential(curvex,p1,p2)
    plt.plot(curvex,curvey,'r', linewidth=2)
    plt.text(.8,8,'y =%0.2f * x ^ %0.2f' %(p1, p2),fontsize=12)    
        
def trendlineLogLinear(xd, yd, order=1, c='r', alpha=1, Rval=False):   
        
    x_data = xd
    y_data = yd

# 1. Transform data into logarithmic space
    log_x = np.log(xd)
    log_y = np.log(yd)

# 2. Fit a straight line: Y = m*X + c
    def linear_func(x, m, c):
        return m * x + c

    popt_log, _ = curve_fit(linear_func, log_x, log_y)

# 3. Transform parameters back to the power-law scale
    b_initial = popt_log[0]           # Slope 'm' is exactly the exponent 'b'
    a_initial = np.exp(popt_log[1])   # Intercept 'c' is ln(a), so we exponentiate it

    print(f"Perfect initial guesses from log-log: a={a_initial:.3f}, b={b_initial:.3f}")

# 4. (Optional) Feed these exact values into the non-linear curve_fit
    def power_law(x, a, b): return a * x**b
    #popt, pcov = curve_fit(power_law, x_data, y_data, p0=[a_initial, b_initial])        
    
    #p1 = popt[0]
    #p2 = popt[1]

# plot curve
    minxd = np.min(xd)
    maxxd = np.max(xd)

    curvex=np.linspace(minxd,maxxd)
    #curvey=power_law(curvex,p1,p2)
    #plt.plot(curvex,curvey,'r', linewidth=1)
    #plt.text(.8,2,'y =%0.2f * x ^ %0.2f' %(p1, p2),fontsize=12)      
        
    #    curvex=np.linspace(.3,200)
    curvey=power_law(curvex,a_initial,b_initial)
    plt.plot(curvex,curvey,'r', linewidth=1)
    plt.text(.8,1,'y =%0.2f * x ^ %0.2f' %(a_initial, b_initial),fontsize=12)  

####################################################################################
#main

import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.optimize import curve_fit
from pylab import rcParams



x=[]
y=[]

with open('LL.csv', 'r') as csvfile:
    plots= csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(float(row[0]))
        y.append(float(row[1]))

trendline(x,y)
trendlineLogLinear(x,y)

plt.loglog(x,y, 'o')

plt.title('Data from the CSV File: People and Expenses')

plt.xlabel('Number of People')
plt.ylabel('Expenses')
plt.grid( which='both', color='0.65', linestyle='-')


plt.show()
plt.savefig('LLplot2.png')
