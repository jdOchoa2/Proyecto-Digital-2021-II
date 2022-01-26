import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import serial

def ReadSave():
    File = open("Data.txt",'w')
    ser = serial.Serial('/dev/cu.usbmodem14101', 9600)
    print("\nReady to go\n")
    for ii in range(3):
        data = str(ser.readline())
        print(data)
        File.write(data[2:(len(data)-5)])
        File.write('\n')
    File.close()

def Multi(LR,LC,CR):
    #Neccesary arrays
    Center = np.zeros(3)
    a = np.zeros(3)
    b2 = np.zeros(3)
    c = np.zeros(3)

    a[0] = LR
    a[1] = LC
    a[2] = CR
    
    #Hiperbola variables
    a[:] *= v/(2e6)
    Center[0] = 0.45
    Center[1] = -9.425
    Center[2] = 9.5
    Center[:] /= 100
    
    c[0] = 38/2
    c[1] = 19.3/2
    c[2] = 18.7/2
    c[:] /= 100
    
    for jj in range(3):
        b2[jj] = c[jj]**2 - a[jj]**2

    #Solution
    A = 1/a[2]**2
    B = -(b2[1]/(b2[2]*a[1]**2))
    C = 1 - (b2[1]/b2[2])

    m2 = A+B
    m1 = -2*(A*Center[2]+B*Center[1])
    m0 = A*Center[2]**2+B*Center[1]**2-C
    #X
    x = -m1/(2*m2)
    det = m1**2-4*m2*m0

    if det < 0:
        print("\nOops! Unexpected error (x), please try again\n")
        return 0, 0;
    
    if a[0]>0:
        if a[2]>0:
            x += math.sqrt(det)/(2*m2)
        else:
            x -= math.sqrt(det)/(2*m2)
    else:
        if a[1]>0:
            x += math.sqrt(det)/(2*m2)
        else:
            x -= math.sqrt(det)/(2*m2)
    #Y
    temp = b2[1]*(((x-Center[1])/a[1])**2-1)
    if temp < 0:
        print("\nOops! Unexpected error (y), please try again\n")
        return 0, 0;
    
    y=-math.sqrt(temp)
    return x*100, y*100;

def Plot(X,Y):
    #Converts list to numpy array
    X = np.array(X)
    Y = np.array(Y)
    #Plotting
    plt.style.use('dark_background')
    circle = plt.Circle((5, -6.7), 4.7, color='b', fill=False)
    
    fig, ax = plt.subplots()
    ax.scatter(X,Y, color='m')
    ax.scatter([-19.3,0,19.3],[0,0,0], color='r')
    ax.set_xlim(-20,20)
    ax.set_ylim(-20,-0)
    ax.set_aspect('equal')
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.grid(linestyle='-', linewidth=0.3)
    ax.add_patch(circle)

    plt.show()
    
### MAIN ###

#Constants
v = 343
#String
new = "y"
#Saves
X=[]
Y=[]
while("y" == new):
        #Comunicates with the Arduino
        ReadSave()
        #Reads data from txt file
        Data = np.loadtxt("Data.txt")
        #Estimates origin point of each sound
        x, y=Multi(Data[0],Data[1],Data[2])
        #Prints when math errors
        if x == 0 and y == 0:
            continue
        print(x)
        print(y)
        #Saves
        X.append(x)
        Y.append(y)
        #Plot
        Plot(X,Y)
        #Asks if it's a valid point
        good = input("\nDo you accept this point? [y/n]")
        if good == 'n':
            del X[-1]
            del Y[-1]
        #Asks to meassure more points
        new = input("Continue? [y/n] ")
