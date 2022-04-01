import matplotlib.pyplot as plt
# plt.rcParams.update({
#   "text.usetex": True,
#   "font.family": "Helvetica"
# })

import numpy as np

from csv import reader
from math import log10, floor

def roundSig(x, sig = 2):
        return round(x, sig-int(floor(log10(abs(x))))-1)


minV = 0.5
maxV = 29.5

maxC = 500.0 # Sanity check

t = []
v = []

M = 0.2  # Define this from the length of the data? After the trim (0.2 seems to work well)
dataSelectionRate = 4

csvFileName = r'C:\Users\tomp\Documents\Python\Cap DC Bias\3NB\3NB CH2 +1 4u7 retest.csv'
#r'C:\Users\tomp\Documents\Python\Cap DC Bias\csvFile.csv'
#'DH Cap Bank 2k.csv'  #"capBankPlusNine"

with open(csvFileName, 'r') as read_obj:
    csvReader = reader(read_obj)
    list = list(csvReader)
    #print(list)

# Find the number of entries in the csv
length = len(list)


# separate the data in a time (t) and voltage (v) list
for x in range(length):
    t.append(float(list[x][0]))
    v.append(float(list[x][1]))


# Trim data
    # Remove data before V =~ 0.5V
    # Remove data after V ~= 30V

print("Raw data length: " + str(length))

for x in range(length):
    if (v[x] > minV):
        lowerDataBound = x
        print("Lower Data Bound: " + str(lowerDataBound))
        break

for x in range(length):
    if (v[length - x - 1] < maxV):
        upperDataBound = length - x - 1
        print("Upper Data Bound: " + str(upperDataBound))
        break

tTrim = []
vTrim = []


for x in range(lowerDataBound, upperDataBound):
    if (x % dataSelectionRate == 0):
        tTrim.append(t[x])
        vTrim.append(v[x])

# print(len(tTrim))
# print(upperDataBound-lowerDataBound)



# Moving average
    # Moving average over M on data of size N
    # Will be N-M entries in the new list 
tAvg = []
vAvg = []
length = len(tTrim)
print("Length of trim: " + str(length))
dataLength = length

MReal = round(length*M)
print("Running average size: " + str(MReal))


M = MReal # redefining M here as I am too lazy to change this for the rest of the script

for x in range(length):
    if (x >= M):
        tTemp = 0
        vTemp = 0
        for y in range(M):
            tTemp += tTrim[x-y]
            vTemp += vTrim[x-y]
        
        tAvg.append(roundSig(tTemp/M, 10))
        vAvg.append(roundSig(vTemp/M, 10))
        
    if(x % round(length/10) == 0): # This progess logic would require non-integer indices to be able to work
        print("Averaging: " + str(round(100*x/length)) + " % done.")
        # print(x/length)

# print(len(tAvg))




# Find capacitance in units of microFarad

C = []

length = len(vAvg)
for x in range(length):
    if (x > 0):
        current = 0.1 # in Amps
        unitConversion = 1000000 # convert to micro
        if (vAvg[x]-vAvg[x-1] != 0):
            tempC = current*unitConversion*(tAvg[x]-tAvg[x-1])/(vAvg[x]-vAvg[x-1])
            if (tempC > 0 and tempC < maxC):
                C.append(tempC)
            else:
                C.append(0)
        else:
            C.append(0)

    # else:
        # C.append(0)
        # del vAvg[0]


    if (x % round(length/5) == 0): # This progess logic would require non-integer indices to be able to work
        print("Finding Capacitance: " + str(round(100*x/length)) + " % done.")


del vAvg[0] # Alligning the C and V data (cannot use this element along anyway)

# Find C at 12V and 24V

C12First = 0
C12Last = 0

C24First = 0
C24Last = 0

length = len(vAvg)
for x in range(length):
    if (vAvg[x] > 11.5 and vAvg[x] < 12.5):
        if (C12First == 0):
            C12First = C[x]
        else:
            C12Last = C[x]
    
    if (vAvg[length - x - 1] > 23.5 and vAvg[length - x - 1] < 24.5):
        if (C24First == 0):
            C24First = C[length - x -1]
        else:
            C24Last = C[length - x -1]


C12Estimate = (C12First + C12Last)/2
C24Estimate = (C24First + C24Last)/2

if (C24Estimate > 0):
    C24 = roundSig(C24Estimate, 3)
else:
    print("24V capactiance measurement error")
    C24 = 0
if (C12Estimate > 0):
    C12 = roundSig(C12Estimate, 3)
else:
    print("12V capactiance measurement error")
    C24 = 0




# plot C vs V

# plt.plot(t, v)
# plt.plot(tTrim, vTrim)
# plt.plot(tAvg, vAvg)
fig = plt.plot(vAvg, C)

titleInfoText = "3NB CH2 +1x4.7" + u"\u03bcF #2"    #"3NB CH2+1x4u7"

plt.title(str(titleInfoText) + " (# points: " + str(dataLength) + ", M = " + str(M) + ", C@12V/24V = " + str(C12) + "/" + str(C24) + u" \u03bcF)")

plt.xlabel("DC Voltage / V")
plt.ylabel("Capacitance / " + u"\u03bcF")

plt.grid()

plt.savefig(r'C:\Users\tomp\Documents\Python\Cap DC Bias\Cap vs V.png')


plt.show()
    # Add gridlines, axis labels, title, axis labels (show 0 and 35V)
    # change colour, data point size
    # Show data length, M, capacitance at 12V/24V

# input('Press ENTER to exit')
