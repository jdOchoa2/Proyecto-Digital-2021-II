# potentiometer_plot.py

import numpy as np
import serial
import time
import matplotlib.pyplot as plt

M = 1000

# make sure the 'COM#' is set according the Windows Device Manager

    
ser = serial.Serial('COM3', 9600)#, timeout=1)
time.sleep(2)



data = []

start = time.time()

for i in range(M):
    line = ser.readline()
    line = str(line)# read a byte string
    #print(line)
    if line:
        
        try:
            dat4 = float(line[2:5])
            print(dat4)
                
            data.append(dat4) # add int to data list
            #time.sleep(0.006)
        except:
            print("ERROR: replace method error")
            
ser.close()

print('DATASHAPE', np.shape(data))

#T = f'Time: {time.time() - start}'

T   = float(time.time() - start)

print(T)

tm = np.linspace(0,T,num=np.shape(data)[0])

    #   build the plot

plt.plot(tm,data)
plt.xlabel('Time')
plt.ylabel('Microphone Reading')
plt.title('Microphone Reading vs. Time')
plt.grid()
plt.show()
   
    

