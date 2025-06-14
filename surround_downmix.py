import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
import math as m

def downmixing(input_file_name):
    data, fs = sf.read(input_file_name, dtype='float32')

    downmixed = np.empty([data.shape[0],2], dtype=np.float32)
    downmixed[:,0] = data[:,0] + data[:,2] / np.sqrt(2) + data[:,4] / np.sqrt(2)
    downmixed[:,1] = data[:,1] + data[:,2] / np.sqrt(2) + data[:,5] / np.sqrt(2)

    outputName = 'downmixed.wav'
    sf.write(outputName, downmixed, fs)
    print(f'OUTPUT FILE: {outputName}')

name = 'test_surround_6_channels.wav'
print(f'INPUT FILE: {name}')
downmixing(name)
