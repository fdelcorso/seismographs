# ###########################################################################
# Program name: savePlotEarthquakesSEISMO
# Author: Francesca Del Corso
# Date: 07/01/2021
# Release: I
#
# This program save SEISMO CHZ earthquakes waveform, FFT and spectrogram plots into the SEISMO1 images dir, given the start date of the event (the end date is 1 minutes after the start date)
# The filenames have the form SEISMO-AAAA-MM-DDTHHMMSS, the default size plot is 800x250 pixels.
#


from os import environ
import numpy as np
from numpy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
from obspy import read
from obspy.core.utcdatetime import UTCDateTime
import obspy.signal
from obspy.signal.konnoohmachismoothing import konno_ohmachi_smoothing
import cv2

import datetime

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

def main(): 

    file = "C:\\temp\\2021.txt"         # da questo file si legge la seconda colonna che contiene l'UTC time dei terremoti di interesse, e da questo calcola lo start_date e l'end_date
    file1 = "C:\\temp\\2020-12-02-1800-00S.S2001_001_CHZ"
    img1 = cv2.imread('C:\\temp\\cavia-subtract.png', cv2.IMREAD_UNCHANGED)

    image_dir = "C:\\temp\\images\\SEISMO1\\waveform\\"
    image_dir_FFT = "C:\\temp\\images\\SEISMO1\\FFT\\"
    image_dir_DATA = "C:\\temp\\images\\SEISMO1\\DATA\\"

    f=open(file,"r")
    lines=f.readlines()
    result=[]                           # result=UTCDateTimes array from the erthquakes file
    for x in lines:
        result.append(x.split('|')[1])
    f.close()

    #for i in range(len(result)):
    # per ogni riga andare su pcseismo in datalog e 

    start_time = UTCDateTime("2020-12-02T18:02:47")
    end_time = UTCDateTime("2020-12-02T18:03:47")                                           # 1 minute after ( da gestire i casi in cui con 1 minuto in più cambia  l'ora o il giorno)
    fileName = "SEISMO1-"+ str("2020-12-02T180247") 
    fileName1 = "SEISMO1-"+str("2020-12-02T180247")  + "-FFT"
    fileName2 = "SEISMO1-"+str("2020-12-02T180247")  + "-spectrogram"

    st = read(file1, starttime=start_time, endtime=end_time)                                # From the 1 hour stream file, we select the [start_time, end_time] period

    # Save waveform (default size: 800x250 pixels)
  
    st.plot(outfile = image_dir+fileName, color='red', tick_format='%I:%M %p')

    # FFT
    spec, freqs = rfft(st[0].data), rfftfreq(st[0].stats.npts, st[0].stats.delta)

    plt.figure(figsize=(12, 6))
    plt.loglog(freqs, np.abs(spec), label="raw", color="grey")
    plt.loglog(freqs, obspy.signal.util.smooth(abs(spec), 5), label="Average")
    plt.loglog(freqs, konno_ohmachi_smoothing(abs(spec), freqs, normalize=True), label="konno ohmachi")

    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Counts")
    plt.legend()
    plt.title("SEISMO1 FFT Plot -"+ str(start_time) + str(end_time))

    # Per figure senza assi, titolo e legenda:
    # plt.legend("")     
    # plt.title("")      # rimane però un quadratino bianco
    # plt.axis('off')
    # plt.loglog(freqs, np.abs(spec), color="grey")
    # plt.loglog(freqs, obspy.signal.util.smooth(abs(spec), 5))
    # plt.loglog(freqs, konno_ohmachi_smoothing(abs(spec), freqs, normalize=True))


    # Save FFT plot

    plt.savefig(image_dir+fileName1)

    # save the spectrogram
    #st[0].spectrogram(outfile = image_dir+fileName2, log=True)  
    

if (__name__ == "__main__"):
    suppress_qt_warnings()
    main()