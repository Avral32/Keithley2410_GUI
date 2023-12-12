import numpy as np
from scipy import misc
from scipy.optimize import newton
import matplotlib.pyplot as plt
# scipy.misc.derivative(func, x0, dx=1.0, n=1, args=(), order=3)[source]
# scipy.misc.derivative - finds the nth derivative of a function at a point x0.
# define Newton's method

def newton_method(f, x, tolerance=1.0e-7):
    """ Uses Newton's method to find a root of f(x) =0 with a guess value x
        """
    while True:
        # iterations
        for _ in range(50):
            x1 = x - f(x) / misc.derivative(f, x)  
            # misc.derivative(f, x) finds derivative at x0
            dx = abs(x1 - x)  
            #print(x, x1)
            if dx < tolerance:
                break
            x = x1
        return x
 
# define a function to be solved
def f(x):
    return (1.0/4.0)*x**3 +(3.0/4.0)*x**2-(3.0/2.0)*x-2
   
   
# guess value x
x=4
# a root of f(x)
x0 = newton_method(f, x)

print('Approximate root x0:' ,x0)
print("Function value at x0 close to zero, f(x0) = ", ((1.0/4.0)*x0**3+(3.0/4.0)*x0**2-(3.0/2.0)*x0-2 ),"\n")

# use scipy.optimize module
def f(x):
    return (1.0/4.0)*x**3 +(3.0/4.0)*x**2-(3.0/2.0)*x-2
    
# guess value   
x=4 
x0 = newton(f,x,fprime=None,args=(),tol=1.4e-6, maxiter=10,fprime2=None)

print("scipy_module" "\n")
print('Approximate root x0:' ,x0)
print("Function value at x0 close to zero, f(x0) = ", ((1.0/4.0)*x0**3+(3.0/4.0)*x0**2-(3.0/2.0)*x0-2 ))

#plot

x = np.arange(-6,4,0.1)
y = (1.0/4.0)*x**3 +(3.0/4.0)*x**2-(3.0/2.0)*x-2
# solution of function f(x)
x0 = [-4,-1,2]
y0 = [0,0,0] 

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
# Move left y-axis and bottim x-axis to centre, passing through (0,0) or center
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
# remove bottom and left axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
# Show ticks in the left and lower axes only
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
# set the color blue
ax.spines['left'].set_color('b')
ax.spines['bottom'].set_color('b')

plt.plot(x,y,'r', label='f(x)', linewidth=0.5)
plt.scatter(x0,y0, marker='o', facecolors='none', edgecolors='r')
plt.xlim(-6,6)
plt.ylim(-20,20)
plt.text(4.1,17, 'f(x)')
plt.text(-4.0, 22,
     r"$f(x)=(1/4)*x^3+(3/4)*x^2-(3/2)*x-2$",
     fontsize=10) 
plt.grid(color='gray', linestyle='--', linewidth=0.2)
plt.show()
