import math
import numpy as np
import matplotlib.pyplot as plt

#Constants
c = 343
L = .15

#Example Initial Conditions
x0 = .05
y0 = .10

print("--------------")
print(x0)
print(y0)

t0L = math.sqrt((x0+L)**2+y0**2)/c
t0C = math.sqrt((x0)**2+y0**2)/c
t0R = math.sqrt((x0-L)**2+y0**2)/c

a = np.zeros(3)
a[0] = (t0L - t0R)*1e6
a[1] = (t0L - t0C)*1e6
a[2] = (t0C - t0R)*1e6

#Hiperbola variables

a[:] *= c/(2e6)

Center = np.zeros(3)
Center[1] = -L/2
Center[2] = L/2

c = np.zeros(3)
c[0] = L
c[1] = L/2
c[2] = L/2

b2 = np.zeros(3)
for i in range(3):
    b2[i] = c[i]**2 - a[i]**2

#Solution
A = 1/a[2]**2
B = -(b2[1]/(b2[2]*a[1]**2))
C = 1 - (b2[1]/b2[2])

m2 = A+B
m1 = -2*(A*Center[2]+B*Center[1])
m0 = A*Center[2]**2+B*Center[1]**2-C

x = -m1/(2*m2)
if a[0]>0:
    if a[2]>0:
        x += math.sqrt(m1**2-4*m2*m0)/(2*m2)
    else:
        x -= math.sqrt(m1**2-4*m2*m0)/(2*m2)
else:
    if a[1]>0:
        x += math.sqrt(m1**2-4*m2*m0)/(2*m2)
    else:
        x -= math.sqrt(m1**2-4*m2*m0)/(2*m2)

y=math.sqrt(b2[1]*(((x-Center[1])/a[1])**2-1))

print("--------------")
print(x)
print(y)
