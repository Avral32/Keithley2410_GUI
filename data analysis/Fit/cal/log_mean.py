# calculate the logarithmic mean of two numbers
import numpy as np

a, b = [ int(x) for x in input('Please eneter the minmum and maxium values ').split(' ')]

# difference of two numbers
x = abs(a- b)
# calculate difference of the natural logarithms (In)
log_x = abs(np.log(a)- np.log(b))

# logarithmic mean value of a and b
log_mean = x / log_x

print('The logarithmic mean value of a and b is :' +  str("{:.2f}".format(log_mean)))