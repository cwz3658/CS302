# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pylab import *

N1, N2 = meshgrid(arange(0, 1000, 1), arange(0, 1000, 1))
k1=600;k2=800;
a1=0.8;a2=2;
r1=1.2;r2=1.1;
rho1=rho2=0;

N1dot=r1*N1*(k1-N1-a2*N2)/k1-rho1;
N2dot=r2*N2*(k2-N2-a1*N1)/k2-rho2;
streamplot(N1, N2, N1dot, N2dot)
show()

N1=arange(0, 1000, 1);
N2=(k1-N1-(k1*rho1)/(r1*N1))/a2;
plot(N1,N2)
show()
N2=arange(0, 1000, 1);
N1=(k2-N2-(k2*rho2)/(r2*N2))/a1;
plot(N1,N2)
xlim([0,1000])
ylim([0,1000])
show()


