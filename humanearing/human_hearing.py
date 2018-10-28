import numpy as np
import pyaudio

#Sampling rate
Fs = 44100    

#Sample lenght in seconds
seconds = 5

#Number of samples for each sound
num_samples = seconds * Fs

#Frequencies to test
frequencies = [5, 10, 20, 40, 60, 100, 200, 300, 400, 500, 1000, 2000, 4000, 8000,
     10000, 12000, 14000, 18000, 20000, 22000 ]
                
#Create the temporal axis 'x' and storage for the computed sinusoidal waves.
#The sound stream we will open expects 1 byte per sample, so set np.int8
x = np.arange( num_samples )
waves = np.zeros( ( len( frequencies ), num_samples ), dtype = np.int8 )

#Calculate the waves for each frequency
for index, f in enumerate( frequencies ):
    #Get a sinusoidal wave
    signal = 100 * np.sin(2 * np.pi * f * x / Fs)
    
    #Save it as 1 byte signed integer
    waves[index, :] = signal.astype( np.int8 )
    
#Open PyAudio handler
p = pyaudio.PyAudio()

#Create a stream to write into. 1 byte (signed) per sample, 1 channel
stream = p.open(format = p.get_format_from_width(1, unsigned = False),
                channels = 1,
                rate = Fs,
                output = True)

#Write to the stream each wave
for index, f in enumerate( frequencies ):
    print( 'Frequency: {:d} Hz.'.format( f) )
    stream.write( waves[index, :] )

# stop and close the stream
stream.stop_stream()
stream.close()

# close PyAudio
p.terminate()