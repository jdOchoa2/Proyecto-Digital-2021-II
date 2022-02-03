import numpy as np
import matplotlib.pyplot as plt

#Importar datos de frequencias 

datf = np.genfromtxt('freqs.csv',delimiter = ',')

f= datf[1:,1]

#f= [1500,2000,1500]

#Importar datos de posición

data = np.genfromtxt('Location.txt',delimiter ="\t")


#Taza

xT = data[0,0]

yT = data[0,1]

rT = data[0,2]

#Golpes

x = data[1:,0]

y = data [1:,1]

#x = [-np.sqrt(2)/2,0 , np.sqrt(2)/2]

#y = [np.sqrt(2)/2 ,1 , np.sqrt(2)/2]

#Transformación al sistema de la taza

#x = x - xT
#y = y - yT

#Evaluación de las frecuencias

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


#Dibujo de taza con diferentes frecuencias

#Circulo
theta = np.linspace(0,2*np.pi,1000)

xC = rT*np.cos(theta)
yC = rT*np.sin(theta)

plt.plot(xC,yC,'k',lw=0.8)

#Puntos

plt.plot(xR,yR,'r.', markersize = 6)

plt.plot(xB,yB,'b.', markersize = 6)

#Rectas

mR = np.array(yR) / np.array(xR)

t = np.linspace(-2,2,500)

for i in range(len(mR)):
    plt.plot(t,t*mR[i],'k--',lw='0.8')

#ejes
plt.axis([-2,2,-2,2])

plt.show()

