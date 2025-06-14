import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
import math as m
import cmath

def downmixing(input_file_name):
    data, fs = sf.read(input_file_name, dtype = 'float32')

    downmixed = np.empty([data.shape[0],2], dtype = np.float32)
    downmixed[:,0] = data[:,0] + data[:,2] / np.sqrt(2) + data[:,4] / np.sqrt(2)
    downmixed[:,1] = data[:,1] + data[:,2] / np.sqrt(2) + data[:,5] / np.sqrt(2)

    outputName = 'downmixed.wav'
    sf.write(outputName, downmixed, fs)
    print(f'OUTPUT FILE: {outputName}')

def phaseShifting(signal, phase):

    ## Fourier transform of real valued signal
    signalFFT = np.fft.rfft(signal)

    ## Get Power Spectral Density
    signalPSD = np.abs(signalFFT) ** 2
    signalPSD /= len(signalFFT) ** 2

    ## Phase Shift the signal +90 degrees
    newSignalFFT = signalFFT * cmath.rect( 1., phase )

    ## Reverse Fourier transform
    newSignal = np.fft.irfft(newSignalFFT)

    return newSignal

def proLogic(input_file_name):
    data, fs = sf.read(input_file_name, dtype = 'float32')

    mixed = np.empty([data.shape[0],2], dtype = np.float32)
    #mixed[:,0] = data[:,0] + data[:,2] / np.sqrt(2) + (data[:,4] + data[:,5]) * np.sin(-30) / np.sqrt(2)
    #mixed[:,1] = data[:,1] + data[:,2] / np.sqrt(2) + (data[:,4] + data[:,5]) * np.sin(30) / np.sqrt(2)
    mixed[:,0] = data[:,0] + data[:,2] / np.sqrt(2) + phaseShifting((data[:,4] + data[:,5]), np.pi/2) / np.sqrt(2)
    mixed[:,1] = data[:,1] + data[:,2] / np.sqrt(2) + phaseShifting((data[:,4] + data[:,5]), -np.pi/2) / np.sqrt(2)

    outputName = 'downmixed_dolby_pro_logic.wav'
    sf.write(outputName, mixed, fs)
    print(f'OUTPUT FILE: {outputName}')

name = 'test_surround_6_channels.wav'
print(f'INPUT FILE: {name}')

# Classic 6-channel -> 2-channel matrix
downmixing(name)

# Dolby Pro Logic 6-channel -> 2-channel matrix
# Do not use with larger files, it clogs memory
proLogic(name)
