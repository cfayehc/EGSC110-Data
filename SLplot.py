# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 15:45:53 2020

@author: cfay
"""

#function definition
#######################################################################################
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

def trendlineSLy(xd, yd, order=1, c='r', alpha=1, Rval=False):        
    
    minxd = np.min(xd)
    maxxd = np.max(xd)
    
# Import curve fitting package from scipy
    from scipy.optimize import curve_fit
    
    def model_func(x, a, b): 
        b_array = np.array(b)
        return a * np.exp(b_array * x)

    popt, pcov = curve_fit(model_func, xd, yd, p0=(1.0, 1.0))
    a_opt, b_opt = popt
    print(f"Optimized a: {a_opt:.4f}, b: {b_opt:.4f}")

# 4. Plot using a semi-logarithmic scale
    plt.semilogy(xd, model_func(xd, *popt), 'r-', label='Fit: $a e^{bx}$')
    plt.text(0.22 * maxxd + 0.2 * minxd, 0.8 * np.max(yd) + 0.2 * np.min(yd),
                 '$y = %0.3f$ exp [%0.3f x]' %(popt[0],popt[1]))


# plot curve
 #   minxd = np.min(xd)
 #   maxxd = np.max(xd)

 #   curvex=np.linspace(.3,200)
  #  curvey=exponential(curvex,p1,p2)
  #  plt.plot(curvex,curvey,'r', linewidth=2)
 #   plt.text(.8,8,'y =%0.2f * x ^ %0.2f' %(p1, p2),fontsize=12)    
        
def trendlineSLLineary(xd, yd, order=1, c='r', alpha=1, Rval=False):   
        
# Import curve fitting package from scipy
    from scipy.optimize import curve_fit        
        
    x_data = xd
    y_data = yd

# 1. Transform data into logarithmic space
    log_x = xd
    log_y = np.log(yd)

# 2. Fit a straight line: Y = m*X + c
    def linear_func(x, m, c):
        return m * x + c

    popt_log, _ = curve_fit(linear_func, log_x, log_y)

# 3. Transform parameters back to the power-law scale
    b_initial = popt_log[0]           # Slope 'm' is exactly the exponent 'b'
    a_initial = np.exp(popt_log[1])   # Intercept 'c' is ln(a), so we exponentiate it

    #print(f"Perfect initial guesses from log-log: a={a_initial:.3f}, b={b_initial:.3f}")

# 4. (Optional) Feed these exact values into the non-linear curve_fit
    def power_law(x, a, b): return a * x**b
    def model_func(x, a, b): 
        b_array = np.array(b)
        return a * np.exp(b_array * x)
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
    curvey=model_func(curvex,a_initial,b_initial)
    plt.plot(curvex,curvey,'r', linewidth=1, linestyle='dashed', color='blue')
   # plt.text(2,1,'y =%0.2f * x ^ %0.2f' %(a_initial, b_initial),fontsize=12)
    plt.text(0.22 * maxxd + 0.2 * minxd, 1 * np.max(yd) + 0.2 * np.min(yd),
                 '$y = %0.3f$ exp [%0.3f x]' %(a_initial,b_initial))


###################################################################################
#main

import matplotlib.pyplot as plt
import numpy as np
import csv

x=[]
y=[]

with open('SL.csv', 'r') as csvfile:
    plots= csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(float(row[0]))
        y.append(float(row[1]))

trendlineSLy(x,y)
trendlineSLLineary(x,y)

plt.semilogy(x,y, 'o')

plt.title('Data from the CSV File: People and Expenses')

plt.xlabel('Frogs')
plt.ylabel('Expenses')
plt.grid(which='both', color='0.65', linestyle='-')

plt.show()
plt.savefig('SLplot.png')