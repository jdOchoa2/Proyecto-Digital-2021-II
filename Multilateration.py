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
    Center[1] = -49/2+0.45
    Center[2] = 49/2+0.45
    Center[:] /= 100
    
    c[0] = 49
    c[1] = 49/2
    c[2] = 49/2
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
        return 0, 0,  a, b2, Center
    
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
        return 0, 0, a, b2, Center
    
    y=-math.sqrt(temp)
    return x*100, y*100, a, b2, Center;

def Plot(X,Y,a,b2,Center):
    #Converts list to numpy array
    X = np.array(X)
    Y = np.array(Y)
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots()

    #Origins
    ax.scatter(X,Y, color='m')
    #Sensors
    ax.scatter([-48.55,0,48.55],[0,0,0], color='r')
    #Cup
    circle = plt.Circle((11.5, -16), 4.7, color='b', fill=False)
    ax.add_patch(circle)
    #Hiperbolas
    xr = np.linspace(-50, 50, 400)
    yr = np.linspace(0, -50, 400)
    xr, yr = np.meshgrid(xr, yr)
    Center[:] *= 100
    a *= 100
    b2 *= 10000
    ax.contour(xr, yr,((xr-Center[0])**2/a[0]**2 - (yr)**2/b2[0]), [1], colors='w', linestyles='dashed', linewidths=0.5)
    ax.contour(xr, yr,((xr-Center[1])**2/a[1]**2 - (yr)**2/b2[1]), [1], colors='w', linestyles='dashed', linewidths=0.5)
    ax.contour(xr, yr,((xr-Center[2])**2/a[2]**2 - (yr)**2/b2[2]), [1], colors='w', linestyles='dashed', linewidths=0.5)

    ax.set_xlim(0,50)
    ax.set_ylim(-50,-0)
    ax.set_aspect('equal')
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.grid(linestyle='-', linewidth=0.3)
   

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
        x, y, a, b2, Center = Multi(Data[0],Data[1],Data[2])
        #Prints when math errors
        if x == 0 and y == 0:
            continue
        print(x)
        print(y)
        #Saves
        X.append(x)
        Y.append(y)
        #Plot
        Plot(X,Y,a,b2,Center)
        #Asks if it's a valid point
        good = input("\nDo you accept this point? [y/n] ")
        if good == 'n':
            del X[-1]
            del Y[-1]
        #Asks to meassure more points
        new = input("Continue? [y/n] ")
