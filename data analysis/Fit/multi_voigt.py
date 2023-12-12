#  Voigt function fit to Data

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.special import wofz, erfc   # wofz -Faddeeva function is a scaled complex complementary error function
import matplotlib.pyplot as plt
from numpy import exp,loadtxt, pi, sqrt
#from lmfit import Model

from scipy.optimize import curve_fit

# load data
data = np.loadtxt('BS1319.txt', skiprows =15, usecols = (0,1))  # usecols=(0,1,2) read selected culumns 1, 2 , 3 cols
x0 = data[:,0]
y0 = data[:,1]
# converts nm to eV
x = 1240 / x0
y = y0

# define guassian fuction
def voigt(x, u, pars):   # pars(parameters)=['a', 'e0', 'sigma0']  # a amplititude
    """define guassian model"""
    a = pars[0]                         # height
    e = pars[1]                        # peak center
    sigma = pars[2]                    # guassian WFHM
    gamma = pars[3]                    #  Lorentz linewidth
    #wofz_1  = a*np.real(wofz((x+1j*gamma0) / sigma0 / sqrt(2))) / (sigma0*sqrt(2*pi)) 
    #function = u + wofz_1
    function = u + a * np.real(wofz((x - e + 1j*gamma) / (sigma*sqrt(2))) * 1 / (sigma*sqrt(2*pi)))
    return function
 
 
# define multi Voigt profiles 
def multi_vp(x, u, *pars):
    """define multi_voigt function for multi peaks"""
    a0 = pars[0]
    a1 = pars[1]
    e0 = pars[2]
    e1 = pars[3]
    sigma0 = pars[4]
    sigma1 = pars[5]
    gamma0 = pars[6]
    gamma1 = pars[7]
	
    peak1 = voigt(x, u, [a0, e0, sigma0, gamma0])
    peak2 = voigt(x, u, [a1, e1, sigma1, gamma1])
	
    return peak1 + peak2
    

variables = ['u', 'a0', 'a1', 'e0', 'e1', 'sigma0', 'sigma1', 'gamma0', 'gamma1'] 

# parameter guess 
# u = 180
# a0 = 700
# a1 =  800
# e0 = 2.7
# e1 = 2.6
# sigma0 = 0.03
# sigma1 = 0.05
# gamma0 = 0.08
# gamma1 = 0.06

pars_guess = (180, 700, 800, 2.7, 2.6, 0.03, 0.05, 0.08, 0.06)
rslt, err = curve_fit(multi_vp, x, y, pars_guess) 
 
# calculate standard errors 
pars_err = np.sqrt(np.diag(err))
 
 
# print results, including best fit parameters and absolute errors 


print('\n', 'Final set of parameters           Standard Error')
print('--------------------------------------------------')
for i in range(len(rslt)):
    parameter = str("{:.6f}".format(rslt[i])) 
    err = str("{:.6f}".format(pars_err[i]))
    variable = str(variables[i])
    if len(variable) == 1:
        print('     ' + variable  + ' ' + '=' + '     ' + parameter.ljust(22) + ('+/-' + ' ' + err).ljust(20))
    elif len(variable) == 2:
        print('    '+ variable + ' ' + '=' + '     ' + parameter.ljust(22) + ('+/-' + ' ' + err).ljust(20))
    elif len(variable) == 6:
        print(variable + ' ' + '=' + '     ' + parameter.ljust(22) + ('+/-' + ' ' + err).ljust(20))
print('--------------------------------------------------')        
        
plt.plot(x,y, marker='+', color = '#4b0082', label='data', markersize=4)
plt.plot(x,voigt(x, rslt[0], [rslt[1], rslt[3], rslt[5], rslt[7]]), 'g--', label='peak1', linewidth=1.0)
plt.plot(x,voigt(x, rslt[0], [rslt[2], rslt[4], rslt[6], rslt[8]]), 'y--', label='peak2', linewidth=1.0)
plt.plot(x,multi_vp(x, *rslt), 'r--', label='best fit', linewidth=1.0)

# set plot
plt.xlim([2.0, 3.1])
plt.grid(color='grey', linestyle='--', linewidth=0.5)

plt.title('Two Voigt functions fit to the experimental data', \
           fontsize = 10, color = 'k', ha = 'center',\
           style = 'italic', weight = 'bold') # ha horizontalalign
           
plt.xlabel('Photon energy (eV)', fontsize = 14)
plt.ylabel('Intensity (arb. units)', fontsize = 14)
plt.legend()
plt.show()
   
   
