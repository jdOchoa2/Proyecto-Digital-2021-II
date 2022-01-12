import math
import numpy as np
import matplotlib.pyplot as plt
import serial
import sys

def ReadSave():
    File = open("Data.txt",'w')
    n=int(sys.argv[1])
    ser = serial.Serial('/dev/cu.usbmodem14101', 9600)
    print(n)
    for ii in range(3*n):
        data = str(ser.readline())
        File.write(data[2:(len(data)-5)])
        File.write('\n')
    File.close()

def Multi(LR,CL,CR):
    #Neccesary arrays
    Center = np.zeros(3)
    a = np.zeros(3)
    b2 = np.zeros(3)
    c = np.zeros(3)

    a[0] = LR
    a[1] = CL
    a[2] = CR
    
    #Hiperbola variables
    
    a[:] *= v/(2e6)
    Center[1] = -L/2
    Center[2] = L/2

    c[0] = L
    c[1] = L/2
    c[2] = L/2

    for jj in range(3):
        b2[jj] = c[jj]**2 - a[jj]**2

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
    return x*100, y*100;

### MAIN ###

ReadSave()

#Constants
v = 343
L = .18

#Read data from txt file
Data = np.loadtxt("Data.txt")
N = int(len(Data)/3)

#Save in
X = np.zeros(N)
Y = np.zeros(N)

#Estimates origin point of each sound
for ii in range(N):
    X[ii],Y[ii]=Multi(Data[ii*3],Data[ii*3+1],Data[ii*3+2])
    print(X[ii])
    print(Y[ii])

plt.scatter(X,Y)
plt.xlim(-10,10)
plt.ylim(0,25)
plt.show()
