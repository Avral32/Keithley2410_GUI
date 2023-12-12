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
data = np.loadtxt('BS2913_18.txt', skiprows =0, usecols = (0,1))  # usecols=(0,1,2) read selected culumns 1, 2 , 3 cols
x0 = data[490:550:,0]
y0 = data[490:550,1]
# converts nm to eV 
x = x0  #1240 / x0
y = y0

# define guassian fuction
def voigt(x, u, pars):  
    """define guassian model"""
    a = pars[0]                       # height
    e = pars[1]                     # peak center
    sigma = pars[2]                  # guassian WFHM
    gamma = pars[3]                  #  Lorentz linewidth
    #wofz_1  = a*np.real(wofz((x+1j*gamma0) / sigma0 / sqrt(2))) / (sigma0*sqrt(2*pi)) 
    #function = u + wofz_1
    function = abs(a) * np.real(wofz((x - e + 1j*gamma) / (sigma*sqrt(2))) * 1 / (sigma*sqrt(2*pi)))
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
	
    return abs(u) + peak1 + peak2
    

variables = ['u', 'a0', 'a1', 'e0', 'e1', 'sigma0', 'sigma1', 'gamma0', 'gamma1'] 

# parameter guess 
u = 0.5
a0 = 2
a1 = 0.1
e0 = 2.67228
e1 = 2.6780832
sigma0 = 0.0005918
sigma1 = 0.00005316
gamma0 = 0.00146
gamma1 = 0.0000003

#strain all guess parameters with 5% bound from the guess values
fit= [u, a0, a1, e0, e1, sigma0, sigma1, gamma0, gamma1]
b_lim = np.zeros((9,2))
#print(b_lim)
for i in range(9):
    if i == 3 or i == 4:
        b_lim[i,0] = fit[i] - np.abs(0.6*fit[i]) # these should be 0.05
        b_lim[i,1] = fit[i] + np.abs(0.6*fit[i])
        #print(b_lim[i,0],b_lim[i,1])
    else:
        b_lim[i,0] = fit[i] - np.abs(0.8*fit[i]) # these should be 0.05
        b_lim[i,1] = fit[i] + np.abs(0.8*fit[i])
        #print(b_lim[i,0],b_lim[i,1])

pars = (u, a0, a1, e0, e1, sigma0, sigma1, gamma0, gamma1)
#pars_bounds=([b_lim[0,0], b_lim[1,0], b_lim[2,0], b_lim[3,0], b_lim[4,0], b_lim[5,0], b_lim[6,0], b_lim[7,0], b_lim[8,0]],\
             #[b_lim[0,1], b_lim[1,1], b_lim[2,1], b_lim[3,1], b_lim[4,1], b_lim[5,1], b_lim[6,1], b_lim[7,1], b_lim[8,0]])
             
pars_bounds=([-np.inf,1,-np.inf,-np.inf,-np.inf,0.0004, -np.inf, 0.001, 0.0000002],\
             [np.inf,3,np.inf,np.inf, np.inf,0.0007, np.inf, 0.002, 0.0000005])
                          
             
rslt, err = curve_fit(multi_vp, x, y, pars, bounds=pars_bounds) 
 
# calculate standard errors 
pars_err = np.sqrt(np.diag(err))
 
# print results, including best fit parameters and absolute errors 

print('\n', 'Final set of parameters           Standard Error')
print('--------------------------------------------------')
for i in range(len(rslt)):
    parameter = str("{:.8f}".format(rslt[i])) 
    err = str("{:.6f}".format(pars_err[i]))
    variable = str(variables[i])
    if len(variable) == 1:
        print('     ' + variable  + ' ' + '=' + '     ' + parameter.ljust(22) + ('+/-' + ' ' + err).ljust(20))
    elif len(variable) == 2:
        print('    '+ variable + ' ' + '=' + '     ' + parameter.ljust(22) + ('+/-' + ' ' + err).ljust(20))
    elif len(variable) == 6:
        print(variable + ' ' + '=' + '     ' + parameter.ljust(22) + ('+/-' + ' ' + err).ljust(20))
print('--------------------------------------------------')        
        
plt.plot(x,y, '+', color = '#4b0082', label='data', markersize=8)
plt.plot(x,voigt(x, rslt[0], [rslt[1], rslt[3], rslt[5], rslt[7]]), 'k--', label='peak1', linewidth=1.0)
plt.plot(x,voigt(x, rslt[0], [rslt[2], rslt[4], rslt[6], rslt[8]]), 'y--', label='peak2', linewidth=1.0)
plt.plot(x,multi_vp(x, *rslt), 'r--', label='best fit', linewidth=1.0)
# guess

#plt.plot(x,multi_vp(x, pars[0], pars[1], pars[2], pars[3],pars[4], pars[5], pars[6], pars[7],pars[8]), \
     #    'b--', label='guess', linewidth=1.0)

# set plot
plt.xlim([2.666, 2.683])
plt.xticks(np.arange(2.666, 2.683, 0.002)) # increment


#plt.text(60, .025, r'$\mu=100,\ \sigma=15$') # plot text
# 注释plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
            # arrowprops=dict(facecolor='black', shrink=0.05),
            # )
#  display a value in plot
   
plt.grid(color='grey', linestyle='--', linewidth=0.5)

plt.title('Two Voigt functions fit to the experimental data', \
           fontsize = 10, color = 'k', ha = 'center',\
           style = 'italic', weight = 'bold') # ha horizontalalign
           
plt.xlabel('Photon energy (eV)', fontsize = 14)
plt.ylabel('Intensity (arb. units)', fontsize = 14)
plt.legend()
plt.show()
   
   
