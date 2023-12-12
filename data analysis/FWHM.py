# find the FWHM of a spectrum

import math
import os
import sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


#os.chdir('C:/Users/Sidik/Desktop/py/measurements/test')
#print(os.getcwd())
sample = input('Please eneter the sample sample: ').upper()
for file in os.listdir():
    
    if file.endswith('.dat')  and file[:6] == sample:         
        data = pd.read_csv(file, sep='.', delimiter='\t',engine='python', skiprows=12,skipfooter=1, header=None)  #thousands='.'
        half_max = data[1].max() / 2
        
        x = data[0]
        y = data[1]
        # find when function crosses line at the half_max
        d = y - half_max
    
        # np.where(cond[x,y]), where True, returns x, otherwise yield y
        idxs = np.where(d > 0)[0]
        
        # indexex of x where y-half_max greater than 0 
        fwhm =  abs(x[idxs[-1]] - x[idxs[0]])            #nm
        FWHM =  abs(1240/x[idxs[-1]] - 1240/x[idxs[0]])  #eV
        FWHM = FWHM.round(4)
                      
        print('The full width at half maximum (FWHM) of the spectrum :', FWHM , 'eV')
                 
plt.figure()
plt.plot(x,y, label='data') # , label = f[:6] 
plt.fill(x[idxs],y[idxs], facecolor='g', alpha=0.4)
plt.xlim([390, 600])
plt.ylim(bottom=0)
plt.text(570,1000, r' $T = 15 K$')
plt.text(400,y.max()-500,'FWHM = %s eV'%FWHM)  # insert variable to plt.text Using % operator
plt.xlabel('Wavelength (nm)', fontsize=12)
plt.ylabel('Intensity (a.u.)', fontsize=12)
plt.tick_params(direction='in',axis='both', top= True, right=True, width=1, pad=3)
plt.legend()
plt.show()