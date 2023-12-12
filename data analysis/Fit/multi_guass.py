
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from numpy import exp,loadtxt, pi, sqrt
#from lmfit import Model

from scipy.optimize import curve_fit


#os.chdir('C:/Users/Sidik Savutjan/Desktop/Py/fit/')
#print(os.getcwd())
data = np.loadtxt('BS1319.txt', skiprows =15, usecols = (0,1))  # usecols=(0,1,2) read selected culumns 1, 2 , 3 cols
x0 = data[:,0]
y0 = data[:,1]

# converts nmto eV
x = 1240 / x0
y = y0


# first emission line
def guass(x, u, pars):   # pars(parameters)=['a', 'e0', 'sigma0']  # u background
    """define guassian model"""
    a = pars[0]                    # amplititude
    e0 = pars[1]                    # center of the peak
    sigma0 = pars[2]                #  FWHM
    function  = u + a*sigma0*sqrt(2*pi)*exp(-(x-e0)**2 / (2*sigma0**2))
    return function
    
    
# define multi peaks

def multi_guass(x,u,*pars):
    """define multi guassians"""
    a = pars[0]                    
    a1 = pars[1]
    e0 = pars[2] 
    e1 = pars[3]
    sigma0 = pars[4]
    sigma1 = pars[5]
    peak1 = guass(x, u, [a, e0, sigma0])
    peak2 = guass(x,u, [a1, e1, sigma1])
    return peak1 + peak2
    
variables = ['u', 'a', 'a1', 'e0', 'e1', 'sigma0', 'sigma1']

#parameters guess
#u=255 
#a=880
#a1=492#
#e0=2.67
#e1=2.77
#sigma0=0.10
#sigma1=0.08

pars_guess = (255, 880, 492, 2.67, 2.77, 0.103, 0.08)
popt, pcov = curve_fit(multi_guass, x, y, pars_guess)

# popt best fit parameters to get the sum of the squared residuals of f(xdata, *popt) - ydata minimized 
# pcov  the estimate covariance of popt, the diognals provide the variance of the parameter emstimation

# calculate the standard errors of parameters
pars_err = np.sqrt(np.diag(pcov))
   
for i in range(len(popt)):
    parameter = str("{:.3f}".format(popt[i])) 
    err = str("{:.4f}".format(pars_err[i]))
    variable = str(variables[i])
    print(variable + ':' + ' ' + ' ' + ' ' + ' ' + parameter + ' ' + err)
 
#for parameters, errs in zip(popt, pars_err):
   # print(str("{:.4f}".format(parameters)) + str("{:.5f}".format(errs)))

plt.figure()

plt.plot(x,y, marker='+', color = '#4b0082', label='data', markersize=6)
plt.plot(x,multi_guass(x, *popt), 'r--', label='best fit', linewidth=1.0)
plt.plot(x,guass(x, popt[0], [popt[1], popt[3], popt[5]]), 'g--', label='peak1', linewidth=1.0)
plt.plot(x,guass(x, popt[0], [popt[2], popt[4], popt[6]]), 'y--', label='peak2', linewidth=1.0)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #  A few typical marker shapes                                    +
    #o - circle                                                       +
    #s - square                                                       +
    #v, <, >, ^ - triangles pointing down, left, right, up            +
    #d, D - thin or thick diamond                                     +
    #x, X - cross (x is line only, X is filled shape)                 +
    #h - hexagon                                                      +
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

plt.xlim([2.0, 3.1])

plt.grid(color='grey', linestyle='--', linewidth=0.5)

plt.title('Two guassian functions fit to the experimental data', \
           fontsize = 10, color = 'k', ha = 'center',\
           style = 'italic', weight = 'bold') # ha horizontalalign
           
plt.xlabel('Photon energy (eV)', fontsize = 14)
plt.ylabel('Intensity (arb. units)', fontsize = 14)
plt.legend()
plt.show()
