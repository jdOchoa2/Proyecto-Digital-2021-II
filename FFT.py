

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from scipy import fftpack

from numpy import genfromtxt
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
plt.text( 500, 60 , 'Frecuencia Máxima: {} Hz'.format(np.round(f1[Y1max+1],2)))
plt.subplots_adjust(hspace=1)

plt.show() 

