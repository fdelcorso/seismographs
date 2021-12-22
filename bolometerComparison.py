# @file bolometerComparison.py
# @Author: Francesca Del Corso
# @date Last Update: 22/12/2021 - previous update: 04/11/2021
# @brief Preso in input un file mseed (o una cartella con più file) ne calcola per ogni ora:
# 1. bin di frequenze e modulo da 0 a 50 Hz 
# 2. Starttime, Endtime, Media, RMS
# Salva i dati su file .txt in out_dir
#
# NOTE:
# For each frequency bin, the magnitude sqrt(re^2 + im^2) tells you the amplitude of the component at the corresponding frequency. 
# The phase atan2(im, re) tells you the relative phase of that component.

# Discrete Fourier Transform: https://numpy.org/doc/stable/reference/routines.fft.html
# numpy.fft.rfftfreq: https://numpy.org/doc/stable/reference/generated/numpy.fft.rfftfreq.html
# numpy.fft.fftfreq: https://numpy.org/doc/stable/reference/generated/numpy.fft.fftfreq.html
# Discrete Fourier transforms (scipy.fft): https://docs.scipy.org/doc/scipy/reference/reference/fft.html#module-scipy.fft
# Plot magnitude_spectrum: 
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.magnitude_spectrum.html#examples-using-matplotlib-pyplot-magnitude-spectrum
              


from obspy import read
import datetime
import matplotlib.pyplot as plt
import numpy as np
from os import environ
import os



def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

def main(): 

    in_dir = "GIGS\\HHZ\\"
    out_dir = "GIGS\\.txt\\"
    ch = "HHZ"
    sta = "GIGS"

    for file in (os.listdir(in_dir)):

        # conterrà i bin delle frequenze e le magnitude
        outResultFile = file.split('.')[0] + "." + sta + "_" + ch + "-Freq+Module.txt"
        outResultFile1 = file.split('.')[0] + "." + sta + "_" + ch + "-Mean+RMS.txt"
        myResults = open(out_dir+outResultFile, "w")   
        myResults.write("#Frequencies, Module" + "\n")         
        myResults1 = open(out_dir+outResultFile1, "w")
        myResults1.write("#Starttime, Endtime, Media, RMS" + "\n")

        # Lettura file .mseed 
        st = read(in_dir+file)
        tr = st[0]   

        # samples in the stream.
        n_sample = len(st)

        # starttime, endtime mseed file 
        starttime=st[0].stats.starttime
        endtime=st[n_sample-1].stats.endtime

        start_time = starttime   
        sec_bin = 3600                 # 1 ora, 240 sec = 4 minuti   

        while (start_time < endtime):

                print(start_time)
                end_time = start_time + sec_bin     

                # Trace slice 
                tr2 = tr.slice(starttime=start_time, endtime=end_time)  

                # Freq
                freq = np.fft.fftfreq(tr2.stats.npts, 1./tr2.stats.sampling_rate)       # bin di frequenza

                # Magnitude (o modulo)
                fft = np.fft.fft(tr2.data)        # parte reale e parte immaginaria
                magn = np.absolute(fft)           # For complex input, a + ib, the absolute value is sqrt{ a^2 + b^2 }

                # Stampa su file csv i bin delle frequenze e i valori del modulo (magnitude) 
                for i in range(len(magn)):
                    myResults.write(str(freq[i]) + "," + str(magn[i]) + "\n")
        
                #plt.plot(freq, magn)
                #plt.show()

                # Media e standard deviation (RMS)
                media = tr2.data.mean()
                std = tr2.data.std()                # equivalente a rms = np.sqrt(np.mean(((st_h[0].data)-media)**2)) 
            
                # Copia media e std in un file
                myResults1.write(str(tr2.stats.starttime) + "," + str(tr2.stats.endtime) + "," + str(media) + "," + str(std) + "\n")

                start_time = end_time 

        myResults.close()     
        myResults1.close()



if (__name__ == "__main__"):

    start = datetime.datetime.now()

    suppress_qt_warnings()
    main()
    
    end = datetime.datetime.now()
    print("Tempo di elaborazione TOTALE:", end-start) 