# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# gnearate random Gaussian values
from random import seed
from random import gauss
#seed random number
seed(5)
mu=10
sigma=0.5

#generate some random numbers

for i in range (20):
	value=gauss(mu,sigma)
	print(value)
	print(value, file=open('gaussian.csv', 'a') )
