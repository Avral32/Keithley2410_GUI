
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import errno
import matplotlib.pyplot as plt

min = 380.    #min wavelength nm 
max = 500.    # max wavelength nm 

sample, power = input('please enter the sample name and the power value ').upper().split(' ')

path = "C:/Users/Sidik/Desktop/py/measurements/15072020"
directory = os.chdir(os.path.join(path,sample))
print(os.getcwd())

# path to save data
path_eval = os.path.join(path, "Eval", sample)

if not os.path.exists(path_eval):
    try:
        os.makedirs(path_eval)
    except OSError as exc:
        if exc.errno != errno.EOFError: 
            raise  

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  sorts files in directory in ascending order 
import re

def avral(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''alist.sort(key=natural_keys) sorts in human order'''
    return [ avral(c) for c in re.split(r'(\d+)', text) ]
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++	

#multi plot arrays 
array_x = np.empty(shape=[0,1024])
array_y = np.empty(shape=[0,1024])

files = []
list = []
         
for file in os.listdir(directory):    
    
    if file[:6] == sample and file[-6:-4] == power:   #power values (1 to 9) file[-5:-4] , power  10 file[-6:-4]
        print(file)
        data = pd.read_csv(file, sep='.', delimiter='\t', skiprows=15, header=None)  #thousands='.'
        idx_min = abs(data[0] - min).values.argmin()  # find the integration range min and max values
        idx_max = abs(data[0] - max).values.argmin()
        integration = data.iloc[idx_max:idx_min, 1].sum().astype(str)
        
        
        list.append(integration)
		
        integ = pd.DataFrame(list)
        integ.to_csv(path_eval +'/' +'Integration_'+ sample+'_power_' + power +'.txt',index=None, header=False)
        print(integration)
		
	    # sore the data in  a array 
        arr_x = np.array(data[0])
        arr_y = np.array(data[1])
        array_x = np.append(array_x, [arr_x], axis=0)
        array_y = np.append(array_y, [arr_y], axis=0)

# plot
row_idx = array_x.shape[0]	
plt.figure()
for i in range(row_idx):
    plt.plot(array_x[i],array_y[i])
plt.xlim([min, max])
plt.ylim(bottom=-10)
plt.xlabel('Wavelength (nm)', fontsize=12)
plt.ylabel('Intensity (a.u.)', fontsize=12)		
plt.show()       
	
print(":::: Have a lot of fun :::")