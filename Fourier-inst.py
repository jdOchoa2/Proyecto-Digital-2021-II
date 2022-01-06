import numpy as np
import serial
import time
import matplotlib.pyplot as plt
import pandas as pd

from scipy import fftpack
from numpy import genfromtxt

#M: Número de datos a tomar
M = 400


   
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

#Lectura datos

data = []

start = time.time()

for i in range(M):
    line = ser.readline()
    line = str(line)
    if line:
        
        try:
            dat4 = float(line[2:5])
            print(dat4)
                
            data.append(dat4) 
        except:
            print("ERROR: replace method error")
            
ser.close()



T   = float(time.time() - start)

print(T)

tm = np.linspace(0,T,num=np.shape(data)[0])

#Gráfica

#plt.plot(tm,data)
#plt.xlabel('Time')
#plt.ylabel('Microphone Reading')
#plt.title('Microphone Reading vs. Time')
#plt.grid()
#plt.show()
   
Table = np.zeros((np.shape(data)[0],2))
print('Table-shape', np.shape(Table))
Table[:,0] = tm
Table[:,1] = data

#Guardar datos

pd.DataFrame(Table).to_csv("FFT/one.csv")

time.sleep(2)

one = genfromtxt('FFT/one.csv', delimiter=',')
#two = genfromtxt('FFT/two.csv', delimiter=',')


t1 = one[1:,1]
y1 = one[1:,2]

N1 = np.shape(t1)[0]

T1 = t1[-1]

print(T1)

Ts1 = T1/N1

Fs1 = (1)/(Ts1)

fstep = Fs1 / N1

fstep2 = 9600 / N1

f1 = np.linspace(0, (N1-1)*fstep2, N1)

Y1 = np.abs(np.fft.fft(y1))/N1


M = int(np.size(np.abs(Y1))/2)

Y1max = np.argmax(np.abs(Y1)[1:M])

print('One-max-freq:', f1[Y1max+1])

plt.subplot(2,1,1)

plt.plot(t1,y1)
plt.title('Amplitud vs. Tiempo')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid()

plt.subplot(2,1,2)
plt.plot(f1,Y1)
plt.title('Abs(Y) vs. Frecuencia')
plt.xlabel('Frecuencia [1/s]')
plt.ylabel('Abs(Y)')
plt.grid()
plt.axis([1500,2500,0,50])
plt.text( 2000, 30 , 'Frecuencia Máxima: {} Hz'.format(np.round(f1[Y1max+1],2)))
plt.subplots_adjust(hspace=1)

plt.show() 