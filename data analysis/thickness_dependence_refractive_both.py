#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 16:13:28 2021

@author: Aha sha
"""

#import sys, getopt
import math
import numpy as np
import matplotlib.pyplot as plt
#import scipy.special as sp

n=10000
#d=50
d=100
n1=2.45
n2=1.0
lam=450.0
pi=np.pi
z=4*pi*n1*d/lam

alpha=np.linspace(0.000001, pi/2, n)
c1=np.cos(alpha)
s1=np.sin(alpha)

tmp=n1*s1/n2

for i in range(0,n):
    if (abs(tmp[i])>1.0):
        tmp[i]=1.0*np.sign(tmp[i])

beta=np.arcsin(tmp)

rs=-np.sin(alpha-beta)/np.sin(alpha+beta)
rp=np.tan(alpha-beta)/np.tan(alpha+beta)

ts=np.sin(2*beta)*np.sin(2*alpha)/np.sin(alpha+beta)**2
tp=c1**2*np.sin(2*beta)*np.sin(2*alpha)/(np.sin(alpha+beta)*np.cos(alpha-beta))**2

tmp=(n1*s1)**2-n2**2
for i in range(0,n):
    if (tmp[i]<0.0):
        tmp[i]=0.0

ps=2.0*np.arctan(np.sqrt(tmp))/(n1*c1)
pp=2*np.arctan(np.sqrt(tmp)/(n2**2*c1))

ii0=np.zeros(200)
ii1=np.zeros(200)
ii2=np.zeros(200)
ii3=np.zeros(200)
ifs=np.zeros(200)
ifp=np.zeros(200)
dd=np.linspace(1,200,200)

for d in range (0,200):
    z=4*pi*n1*d/lam
    p0=1+rs**2+2.0*rs*np.cos(z*c1+ps)
    ii0[d]=np.dot(p0,s1)*pi/(2*n)
    p1=(1+rp**2+2.0*rp*np.cos(z*c1+pp))*c1**2
    ii1[d]=np.dot(p1,s1)*pi/(2*n)
    p2=1+rs**2+2.0*rs*np.cos(z/c1+ps)
    ii2[d]=np.dot(p2,s1)*pi/(2*n)
    p3=(1+rp**2+2.0*rp*np.cos(z/c1+pp))*c1**2
    ii3[d]=np.dot(p3,s1)*pi/(2*n)
    ifs[d]=np.dot(ts,s1)*pi/(2*n)
    ifp[d]=np.dot(tp,s1)*pi/(2*n)

ialt=ii0+ii1
ineu=ii2+ii3

plt.figure()

plt.subplot(221)
plt.xlabel('thickness')
plt.ylabel('intensity')
plt.title('$a \cdot cos(\Theta)$',pad=6)
plt.plot(dd,ii0,dd,ii1,dd,ialt,dd,ifs)
plt.subplot(222)
plt.xlabel('thickness')
#plt.ylabel('intensity')
plt.title('$a / cos(\Theta)$',pad=6)
plt.plot(dd,ii2,dd,ii3,dd,ineu,dd,ifp)
#plt.show()
plt.savefig("refractive.pdf")
