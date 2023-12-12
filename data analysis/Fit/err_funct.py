
# Knife-edge technique to determine the laser spot size,
# this script fits the experimetal data to the err function to get the beam waist

from scipy.special import erfc
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from numpy import exp,loadtxt, pi, sqrt
from pathlib import Path
import numpy as np
import pandas as pd
import os

# load data
path = os.chdir('C:/Measurements/Savutjan/18062020/19062020/test')
data = np.loadtxt('data.txt', skiprows =0, usecols = (0,1))
x = data[:,0]
y = data[:,1]

# define err function

def err_funct(x,u, x_0, w_0):
    """ define the err function with parameters of beams center x_0,
    beam waist w_0.
    """
    #x_0    beam center
    #w_0     beam waist
    #u amplitude
    function = u*1/2*(1+erfc((x-x_0)/(sqrt(2)*w_0)))
    return function
    
          
#guess para
u = 1
x_0 = 40
w_0 = 10

pars_guess = (u, x_0, w_0)
rslt, err = curve_fit(err_funct,x,y, pars_guess)
#pars_err = np.sqrt(np.diag(err))
  
rslt = rslt.round(1)   
print(rslt)  
    
    
plt.figure()
plt.scatter(x,y, marker='x', color='k')

plt.plot(x,err_funct(x, *rslt), 'r--', label='best fit', linewidth=1.0)
plt.ylim(bottom=0)
plt.xlim(-1,100)
plt.title('Knife_edge - Err function fit to experimental data', \
           fontsize = 10, color = 'k', ha = 'center',\
           style = 'italic') #, weight = 'bold'
plt.xlabel('Position (\u03bcm)', fontsize=12)
plt.ylabel('Intensity (a.u.)', fontsize=12)	
plt.ylabel('Intensity (a.u.)', fontsize=12)	
#textu*1/2*(1+erfc((x-x_0)/(sqrt(2)*w_0)))
plt.text(50,0.9, '$ fit = u /2*(1+erf(x-x_0)/(\sqrt{2}*w_0)) $')
plt.text(50,0.85, 'beam center:' + ' '+ str(rslt[1]) + '$\mu m$') 
plt.text(50,0.80, 'beam waist:' + ' ' + str(rslt[2]) + '$\mu m$')
plt.savefig('beam_size.pdf')
plt.show()