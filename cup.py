import numpy as np
import matplotlib.pyplot as plt

#Importar datos de frequencias 
datf = np.genfromtxt('freqs.csv',delimiter = ',')
f= datf[1:,1]
#Importar datos de posición
data = np.genfromtxt('position.csv',delimiter =',')
#Información de la taza (Coordenadas de centro y radio)
xT = data[1,1]
yT = data[1,2]
rT = data[1,3]
#Golpes
x = data[2:,1]
y = data [2:,2]
#Transformación al sistema de la taza
x = x - xT
y = y - yT
#Clasificación de las frecuencias en altas (azules) y bajas (rojas)
r_index = []
b_index = []
for i in range(len(f)):
    if f[i] < 1900:
        r_index.append(i)
    else:
        b_index.append(i)
print(r_index)
print(b_index)
xR = []
yR = []
xB = []
yB = []
for i in r_index:
    xR.append(x[i])
    yR.append(y[i])
for i in b_index:
    xB.append(x[i])
    yB.append(y[i])
"""Dibujo de taza con diferentes frecuencias"""
#Borde de la taza
theta = np.linspace(0,2*np.pi,1000)
xC = rT*np.cos(theta)
yC = rT*np.sin(theta)
plt.plot(xC,yC,'k',lw=0.8)
#Puntos
plt.plot(xR,yR,'r.', markersize = 6)
plt.plot(xB,yB,'b.', markersize = 6)
#Ejes en dónde se puede encontrar el asa
mR = np.array(yR) / np.array(xR)
t = np.linspace(-2-rT,2+rT,1000)

for i in range(len(mR)):
    plt.plot(t,t*mR[i],'k--',lw='0.8')
    
    if len(xR)==1: 
        plt.plot(t,-t/(mR[i]),'k--',lw='0.8')
        
plt.axis([-2-rT,2+rT,-2-rT,2+rT])
plt.show()
