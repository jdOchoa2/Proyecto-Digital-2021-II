
""" Ejecutar como:  python3 Origins.py <Coordenada Centro Taza X (cm)> <Coordenada Centro Taza Y (cm)> <Temperatura (ºC)> """

import sys
import math
import serial
import numpy as np
import sympy as sym
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sympy.solvers import solve

def ReadSave():
    """-----------------------------------------------
    ReadSave:
    Se comunica con el arduino y guarda los datos del
    puerto serial en Data.txt.
    -----------------------------------------------"""
    File = open("Data.txt",'w')
    ser = serial.Serial('/dev/cu.usbmodem14101', 9600)
    print("\nReady to go\n")
    for ii in range(3):
        data = str(ser.readline())
        File.write(data[2:(len(data)-5)])
        File.write('\n')
    File.close()
    
def Secants(LR, LC, CR, cup, radius):
    """----------------------------------------------------------
    Secants:
    Dadas las diferencias de tiempo entre sensores, encuentra
    los posibles origenes del sonido sobre la circunferencia 
    de la taza mediante la intercepción de hipérbolas.
    -------------------------------------------------------------
    Argumentos:
     * LR     : diferencia tiempo sensor izquierdo-derecho
               (microsegundos)
     * LC     : diferencia tiempo sensor izquierdo-centro
               (microsegundos)
     * CR     : diferencia tiempo sensor centro-derecha
               (microsegundos)
     * cup    : coordenadas centro de la taza
     * radius : radio de la taza
    --------------------------------------------------------------
    Return:
     * Ix,Iy         : Arrays con las coordenadas de los origenes
     * a, b2, Center : Arrays con parámetros de las hipérboelas
    -----------------------------------------------------------"""
    #Convierte unidades a metros
    Cup = [0,0]
    for ii in range(2):
        Cup[ii] = cup[ii] / 100
    Radius = radius/100
    #Arreglos necesarios para guardar información
    Center = np.zeros(3)
    a = np.zeros(3)
    b2 = np.zeros(3)
    c = np.zeros(3)
    Ix = []
    Iy = []
    #Llena los arreglos con los párametros de la taza
    a[0] = LR
    a[1] = LC
    a[2] = CR
    a[:] *= v/(2e6) #Convierte tiempos a distancias en metros
    Center[0] = 0.45
    Center[1] = -49/2+0.45
    Center[2] = 49/2+0.45
    Center[:] /= 100
    c[0] = 49
    c[1] = 49/2
    c[2] = 49/2
    c[:] /= 100
    #Encuentra la intercepción de cada hipérbole con la taza usando sympy
    P = sym.Symbol('P', real = "True")
    for jj in range(3):
        b2[jj] = c[jj]**2 - a[jj]**2
        Solution = solve( (P-Cup[0])**2 + (-sym.sqrt( b2[jj]*( (P-Center[jj])**2 / a[jj]**2 - 1))-Cup[1])**2 - Radius**2, P)
        for kk in Solution:
            #Simplifica la solución y la guarda en un arreglo
            xs = sym.N(kk)
            Ix.append(xs*100) #Convierte a centímetros
            ys = -math.sqrt(b2[jj]*( (xs-Center[jj])**2 / a[jj]**2 -1))
            #Descarte puntos en el hemisferio sur de la taza
            if ys < Cup[1]:
                Ix.pop(-1)
            else:
                Iy.append(ys*100) #Convierte a centímetros 
    return Ix, Iy, a, b2, Center
        
def Plot(X,Y,a,b2,Center,cup,radius):
    """----------------------------------------------------------
    Plot:
    Grafica de la sección transversal de la taza, las hipérbolas
    que la atraviesan y los puntos de origen.
    -------------------------------------------------------------
    Argumentos:
     * X,Y           : Coordenadas de los puntos de origen (cm)
     * a, b2, Center : Arrays con parámetros de las hipérbolas
     * cup           : coordenadas centro de la taza
     * radius        : radio de la taza
    -----------------------------------------------------------"""
    #Convierte las listas a arrays de numpy
    X = np.array(X)
    Y = np.array(Y) 
    plt.style.use('dark_background') #Fondo negro
    fig, ax = plt.subplots()
    #Origenes
    ax.scatter(X,Y, color='m')
    #Sensores (normalmente fuera de plano)
    ax.scatter([-48.55,0,48.55],[0,0,0], color='r') 
    #Taza
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
    #Parámetros de la gráfica
    xlim_d = cup[0] - 3*radius
    xlim_u = cup[0] + 3*radius
    ylim_d = cup[1] - 3*radius
    ylim_u = cup[1] + 3*radius
    ax.set_xlim(xlim_d,xlim_u)
    ax.set_ylim(ylim_d,ylim_u)
    ax.set_aspect('equal')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.grid(linestyle='-', linewidth=0.3)
    plt.show()

def mid_point(X,Y,cup,radius):
    """----------------------------------------------------------
    mid_point:
    Encuentra el punto medio sobre la taza entre los puntos 
    suministrados
    -------------------------------------------------------------
    Argumentos:
     * X,Y           : Coordenadas de los puntos de origen (cm)
     * cup           : coordenadas centro de la taza
     * radius        : radio de la taza
    -------------------------------------------------------------
    Return:
     * Point         : Coordenadas del punto medio (cm)
    -----------------------------------------------------------"""
    mean_theta = 0
    for ii in range(len(X)):
        mean_theta += math.atan( (X[ii] - cup[0]) / (Y[ii] - cup[1]) )
    mean_theta /= len(X)
    Point = [ radius*math.sin(mean_theta) + cup[0], radius*math.cos(mean_theta) + cup[1]]
    return  Point

def print_array(A):
    """----------------
    Imprime el array A
    -----------------"""
    for ii in A:
        print("{:.2f}".format(ii),"\t",end="")
    print()
    
"""---------------------------
             MAIN
---------------------------"""
v = 331 * math.sqrt( 1 - (int(sys.argv[3]) / 273) )  #Rapidez del sonido
cup = [int(sys.argv[1]), int(sys.argv[2])] #Posición del centro de la taza
radius = 4.1 #radio de la taza
#Se guarda la información de la taza
Sx = [cup[0]]
Sy = [cup[1]]
new = "y" #string para continuar mediciones
while("y" == new):
        #Comunicación con el arduino
        #ReadSave()
        #Lee información de Data.txt
        Data = np.loadtxt("Data.txt")
        #Estima el punto de origen un golpe a la taza
        print("Finding point. This could take a while...")
        X,Y,a,b2,Center = Secants(Data[0],Data[1],Data[2],cup,radius)
        if not len(X) == 0:
            #Encuentra el punto medio
            Mean = mid_point(X,Y,cup,radius)
            Plot([Mean[0]],[Mean[1]],a,b2,Center,cup,radius)
            accept = input("Do you accept this point? [y/n] ")
            if ("y" == accept):
                #Guarda el punto
                Sx.append(Mean[0])
                Sy.append(Mean[1])
            else:
                #Retorna todas las intersecciones detectadas para escoger manualmente
                print_array(X)
                print_array(Y)
                Plot(X,Y,a,b2,Center,cup,radius)
                select = input("Select a point (n for none): ")
                if  select  in  {"0","1","2","3","4","5"}:
                    #Guarda el punto
                    Sx.append(X[int(select)])
                    Sy.append(Y[int(select)])
        #Pregunta para hacer más mediciones
        new = input("Continue? [y/n] ")
#Guarda en  position.csv
print("Saving in position.csv...")
Table = np.zeros((len(Sx),3))
Table[:,0] = Sx
Table[:,1] = Sy
Table[0,2] = radius
pd.DataFrame(Table).to_csv("position.csv")

