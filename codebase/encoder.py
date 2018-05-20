# This file contains the encoder

# import modules
import numpy as np
from scipy.io import wavfile
from scipy import fftpack 
from scipy import stats
import matplotlib.pyplot as plt

# Parameters
path = '../samples/heyhey01.wav'
bl_size = 128

# read wavefile
fs, data = wavfile.read(path)
data = np.ravel(data)

# divide data in blocks
l_over = len(data)%bl_size
rest = data[len(data)-l_over :]
data = data[: len(data)-l_over]
blocks = [data[i:i+bl_size] for i in range(0, len(data), bl_size)]

# transform blocks with DTC and Quantize them
for i in range(0,len(blocks)):
	blocks[i] = fftpack.dct(blocks[i], norm='ortho')
	#blocks[i] = stats.threshold(blocks[i], threshmin=1)
	blocks[i] = blocks[i]/16
	blocks[i] = blocks[i] + 0.5
	blocks[i] = blocks[i].astype(int)
	#blocks[i] = np.clip(blocks[i], None, 256)

print blocks

# decoding for testing
for i in range(0,len(blocks)):
	blocks[i] = blocks[i]*16
	blocks[i] = fftpack.idct(blocks[i], norm='ortho')
	blocks[i] = blocks[i].astype(int)

'''
signal = blocks[0]
for i in range(1,len(blocks)):
	signal[i*bl_size/2 :] = (signal[i*bl_size/2 : ] + blocks[i][ : bl_size/2 ])/2
	signal = np.append(signal, blocks[i][bl_size/2 :])
'''
signal = np.array([])
for b in blocks:
	signal = np.append(signal, b)

print len(signal)
print len(data)

import math
msqer = 0
for i in range(0,len(signal)):
	msqer += (data[i]-signal[i])**2
msqer = msqer/len(signal)

print ("SNR: ", 10*math.log10(np.var(data)/msqer))
