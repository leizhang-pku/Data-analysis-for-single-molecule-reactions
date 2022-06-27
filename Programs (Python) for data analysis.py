import numpy as np
import matplotlib.pyplot as plt
import csv

# extract data from original data file
file = "./PhBr.txt"   # the data are from the Mizoroki-Heck reaction between PhBr and styrene at 298 K
t = np.loadtxt(file, delimiter=None, dtype="float")
t1 = t[:, 0]   # extract column 1 (time) in original data file
t2 = t[:, 1]   # extract column 2 (current) in original data file

# idealisation of the current signal
t2[t2 < 175] = 1   # the lowest current level is defined as current level 1
t2[t2 > 253] = 4   # the highest current level is defined as current level 4
i = 0
while i < 576000:
    if 187 < t2[i] <= 203:
        t2[i] = 3   # the current values between 187 and 203 nA (these values vary at different reaction conditions) are defined as current level 3
    if 175 <= t2[i] <= 187:
        t2[i] = 2   # the current values between 175 and 187 nA (these values vary at different reaction conditions) are defined as current level 2
    i += 1
t1 = list(t1)   # convert t1 to list data
t2 = list(t2)   # conver t2 to list data

# generate current level transformation sequences and record the time position of transformation
t3 = list()     # create new column for t3 (sequences)
change_position = list()   # create new list for the time position of transformation
i = 0
while i < 575999:
    if t2[i] != t2[i+1]:
        t3.append(t2[i])
        change_position.append(i)
    i += 1
t3.append(t2[i])   # record the last current level within the data, assign as t3
t3 = list(map(int, t3))  # convert t3 to integer data
print(t3)   # print the current level transformation sequences
print(len(t3))   # print the length of t3
print(change_position)   # print the time position of transformation
# the sequences and the time position of transformation can be used to analyze the dwell time and kinetics of Mizoroki-Heck reaction


# Search specific current transformation and can be used for reversibility study
A = [1, 3, 4, 2, 1]   # set a sequence (any sequence can be set)
i = 0
a = 0
for i in range(0, len(t3)-len(A)+1):   # if the sequence exist, it will be counted as a
    if A == t3[i:i+len(A)]:
        a += 1
print('There are', a, ' sequences of 13421.')

# Record specific current transformation
A = [1, 3, 4, 2, 1]   # set a sequence (any sequence can be set)
A_start_position = []
A_end_position = []
a = 0
for i in range(0, len(t3)-len(A)+1):   # if the sequence exist, it will be counted as a
    if A == t3[i:i+len(A)]:
        a += 1
        A_start_position.append(change_position[i])
        A_end_position.append(change_position[i+len(A)])

# extract corresponding original data of the specific sequence, and record in csv. file.
t2 = t[:, 1]   # extract column 3 (current signals)
for i in range(a):
    b = A_end_position[i] - A_start_position[i]
    b = int(b)
    filename = 'Br_13421_' + str(i+1) + '.csv'
    csvFile = open(filename, 'w', newline='')
    try:
        writer = csv.writer(csvFile)
        for j in range(int(b+57599*0.02)):
            writer.writerow((t1[int(A_start_position[i] - 57600*0.01 + j)], t2[int(A_start_position[i]-57600*0.01+j)]))
    finally:
        csvFile.close()
