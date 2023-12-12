# The script is used to calculate the angular dependent dipole emission for different 
# polarization direction implemented by Sidik, following the thesis by Manfred Fleck, 1969
import math
import numpy as np
import matplotlib.pyplot as plt
from numpy import sin, cos,tan, pi, arcsin, arange, sqrt,arctan
import colorama
from colorama import Fore, init
init()
n=100
#d=50
d=100
n1=2.6
n2=1.0
#n2=1.78
lam=450.0
pi=np.pi
z=4*pi*n1*d/lam

alpha=np.linspace(0.01, pi/2, n)
c1=np.cos(alpha)
s1=np.sin(alpha)

tmp=n1*s1/n2
#tmp = n2*s1/n1
for i in range(0,n):
    if (abs(tmp[i])>1.0):
        tmp[i]=1.0*np.sign(tmp[i])
    if (tmp[i] < 0.0):
        tmp[i] = 0.0

beta=np.arcsin(tmp)

#reflection coefficients
rs=-sin(alpha-beta)/sin(alpha+beta)
rp=tan(alpha-beta)/tan(alpha+beta)

ts=2*sin(beta)*cos(alpha)/sin(alpha+beta)
tp=2*sin(beta)*cos(alpha)/(sin(alpha+beta)*cos(alpha-beta))


# phase shift with dipoles polarized parallel and perpendicular to the plane of  incidence
#ps=-2.0*np.arctan(sqrt(tmp))/(n1*c1)
ps = -2.0*arctan(sqrt(tmp))/(n1*c1)
pp=-2*arctan(sqrt(tmp)/(n2**2*c1))

I_a = np.zeros(210)
I_b = np.zeros(210)
I_c = np.zeros(210)

dd=np.linspace(1,210,210)

#print(Fore.YELLOW+"theta:",tmp)
pa= 1+rs**2 + 2*rs*cos((z*c1)-ps)
pp = c1**2*(1+rs**2 + 2*rs*cos((z*c1)-pp))
print(pa)
for d in range (0,210):
    z=4*pi*n1*dd[d]/lam
    pa= 1+rs**2 + 2*rs*cos((z*c1)-ps)
    I_a[d] = np.sum(pa)
    #print("d", d, "I_a:", pa)
    pb = c1**2*(1+rs**2 + 2*rs*cos((z*c1)-pp))
    I_b[d] = np.sum(pb)
    pc = s1**2*(1+rs**2 + 2*rs*cos((z*c1)-pp))
    I_c[d] = np.sum(pc)

dp = np.stack((dd, I_a), axis=0)
dp = np.transpose(dp)
#np.savetxt('data_Ia.dat', dp, delimiter = ' ')
#p = I_b+I_c
I_ps = I_b + I_a # perpendicular to the surface
I_s = I_c
#plt.plot(dd,I_ps, label='diple axis perpendicular to the plane of incidence')
#plt.plot(dd, I_c, 'r', label='dipole axis in the plane of incidence perpendicular to surface')
plt.plot(alpha*180/pi, pa)
#plt.plot(dd, p, 'b')
#plt.plot(dd, I_c, 'k')


plt.xlabel('Thickness /nm')
plt.ylabel('Intensity / arb. units')
plt.title('GaN cap thickness dependence of PL intensity',pad=6)
plt.legend()
plt.show()