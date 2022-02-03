import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sympy.solvers import solve
import sympy as sym
import serial
import sys

def ReadSave():
    File = open("Data.txt",'w')
    ser = serial.Serial('/dev/cu.usbmodem14101', 9600)
    print("\nReady to go\n")
    for ii in range(3):
        data = str(ser.readline())
        File.write(data[2:(len(data)-5)])
        File.write('\n')
    File.close()
    
def Secants(LR, LC, CR, cup, radius):
    #Units to meters
    Cup = [0,0]
    for ii in range(2):
        Cup[ii] = cup[ii] / 100
    Radius = radius/100
    #Neccesary arrays
    Center = np.zeros(3)
    a = np.zeros(3)
    b2 = np.zeros(3)
    c = np.zeros(3)
    Ix = []
    Iy = []
    #Hyperbola variables
    a[0] = LR
    a[1] = LC
    a[2] = CR
    a[:] *= v/(2e6)

    Center[0] = 0.45
    Center[1] = -49/2+0.45
    Center[2] = 49/2+0.45
    Center[:] /= 100
    
    c[0] = 49
    c[1] = 49/2
    c[2] = 49/2
    c[:] /= 100

    #Sympy solution to the system
    P = sym.Symbol('P', real = "True")
    for jj in range(3):
        b2[jj] = c[jj]**2 - a[jj]**2
        #Points of the cup that intercept each all the hyperbolas
        Solution = solve( (P-Cup[0])**2 + (-sym.sqrt( b2[jj]*( (P-Center[jj])**2 / a[jj]**2 - 1))-Cup[1])**2 - Radius**2, P)
        for kk in Solution:
            #Symplify solution
            xs = sym.N(kk)
            Ix.append(xs*100)
            ys = -math.sqrt(b2[jj]*( (xs-Center[jj])**2 / a[jj]**2 -1))
            #Discard points
            if ys < Cup[1]:
                Ix.pop(-1)
            else:
                Iy.append(ys*100) 
    return Ix, Iy, a, b2, Center
        
def Plot(X,Y,a,b2,Center,cup,radius):
    #Converts list to numpy array
    X = np.array(X)
    Y = np.array(Y) 
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    #Posible origins
    ax.scatter(X,Y, color='m')
    #Sensors
    ax.scatter([-48.55,0,48.55],[0,0,0], color='r')
    #Cup
    circle = plt.Circle((cup[0], cup[1]), radius, color='b', fill=False)
    ax.add_patch(circle)
    #Hiperbolas
    xr = np.linspace(-100, 100, 400)
    yr = np.linspace(0, -100, 400)
    xr, yr = np.meshgrid(xr, yr)
    Center[:] *= 100
    a *= 100
    b2 *= 10000
    ax.contour(xr, yr,((xr-Center[0])**2/a[0]**2 - (yr)**2/b2[0]), [1], colors='w', linestyles='dashed', linewidths=0.5)
    ax.contour(xr, yr,((xr-Center[1])**2/a[1]**2 - (yr)**2/b2[1]), [1], colors='w', linestyles='dashed', linewidths=0.5)
    ax.contour(xr, yr,((xr-Center[2])**2/a[2]**2 - (yr)**2/b2[2]), [1], colors='w', linestyles='dashed', linewidths=0.5)
    Center[:] /= 100
    a /= 100
    b2 /= 10000
    ax.set_xlim(0,30)
    ax.set_ylim(-80,-50)
    ax.set_aspect('equal')
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.grid(linestyle='-', linewidth=0.3)
    plt.show()

def print_array(A):
    for ii in A:
        print("{:.2f}".format(ii),"\t",end="")
    print()

def mid_point(X,Y,cup,radius):
    mean_theta = 0
    for ii in range(len(X)):
        mean_theta += math.asin((X[ii] - cup[0])/(Y[ii] - cup[1]))
    mean_theta /= len(X)
    Point = [ radius*math.sin(mean_theta) + cup[0], radius*math.cos(mean_theta) + cup[1]]
    return  Point
    
### MAIN ###

#Constants
v = 343
#Save
new = "y"
#Cup center
cup = [int(sys.argv[1]), int(sys.argv[2])]
radius = 4.1
#Save cup information to file
SaveFile = open("Location.txt",'w')
SaveFile.write(str(cup[0]))
SaveFile.write("\t")
SaveFile.write(str(cup[1]))
SaveFile.write("\t")
SaveFile.write(str(radius))
SaveFile.write("\n")

while("y" == new):
        #Comunicates with the Arduino
        ReadSave()
        #Reads data from txt file
        Data = np.loadtxt("Data.txt")
        #Estimates origin point of each sound
        print("Finding point. This could take a while...")
        X,Y,a,b2,Center = Secants(Data[0],Data[1],Data[2],cup,radius)
        print(X)
        print(Y)
        Plot(X,Y,a,b2,Center,cup,radius)
        #Finds Mid_Point
        if not len(X) == 0:
            #Mean = mid_point(X,Y,cup,radius)
            Mean = [0,0]
            Plot([Mean[0]],[Mean[1]],a,b2,Center,cup,radius)
            accept = input("Do you accept this point? [y/n] ")
            if ("y" == accept):
                #Saves to file
                SaveFile.write(str(Mean[0]))
                SaveFile.write("\t")
                SaveFile.write(str(Mean[1]))
                SaveFile.write("\n")
            else:
                print_array(X)
                print_array(Y)
                Plot(X,Y,a,b2,Center,cup,radius)
                select = input("Select a point (n for none): ")
                if  select  in  {"0","1","2","3","4","5"}:
                    #Saves to file
                    SaveFile.write(str(X[int(select)]))
                    SaveFile.write("\t")
                    SaveFile.write(str(Y[int(select)]))
                    SaveFile.write("\n")
        #Asks to meassure more points
        new = input("Continue? [y/n] ")
print("Saving in Location.txt...")
SaveFile.close()
