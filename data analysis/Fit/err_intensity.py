
# calculate average power values of attenuator wheel (10 values)

import pandas as pd
import numpy as np
from numpy import sqrt
import sys
import os
import re
import csv

sample = (input('Please enter the sample name ')).upper()

path = 'C:/Users/Sidik Savutjan/Desktop/py/measurements/15072020/eval'
directory = os.chdir(os.path.join(path,sample))
print(os.getcwd())


def avral(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''alist.sort(key=natural_keys) sorts in human order'''
    return [ avral(c) for c in re.split(r'(\d+)', text) ]

files = []

array_err = np.empty(shape=[0,1])
array_intensity = np.empty(shape=[0,1])

# order file in number sequences
for file in os.listdir():
    files.append(file)
    files.sort(key =natural_keys)

for file in files:
    if file.endswith('.txt'):
        #print(file)
        data = pd.read_csv(file, delimiter='/t',engine='python', skiprows=0, header=None, )#usecols=(0,1)
        #print(data)
	
		# standard err
        err = data.std() 
		# poisson err sqrt(data)
        err_p = data.apply(np.sqrt)
        mean_err_p = err_p.mean()
        err_sum = sqrt(err**2 + mean_err_p**2)
        
        array_intensity = np.append(array_intensity,[data.mean()], axis=0)
        array_err = np.append(array_err, [err_sum], axis=0)        
               		
err_total = pd.DataFrame(array_err)
mean_int = pd.DataFrame(array_intensity)
total = pd.concat([mean_int,err_total], axis=1, ignore_index=True)
total = total.round(4) 
total.columns =['Mean PL','Err_sum']   
print(array_intensity,array_err)
total = total.iloc[::-1]
total.to_csv('mean_err_sum_' + sample + '.dat.',sep =' ',index=None, header=True, quoting=csv.QUOTE_NONE, escapechar=' ')			
print('Done!')