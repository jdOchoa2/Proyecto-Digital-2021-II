
import numpy as np
import serial
import time
import matplotlib.pyplot as plt
import pandas as pd

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

plt.plot(tm,data)
plt.xlabel('Time')
plt.ylabel('Microphone Reading')
plt.title('Microphone Reading vs. Time')
plt.grid()
plt.show()
   
Table = np.zeros((np.shape(data)[0],2))
print('Table-shape', np.shape(Table))
Table[:,0] = tm
Table[:,1] = data

#Guardar datos

pd.DataFrame(Table).to_csv("FFT/one.csv")

    

