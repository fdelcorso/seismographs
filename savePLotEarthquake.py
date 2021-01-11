# ###########################################################################
# Program name: savePlotEarthquakes
# Author: Francesca Del Corso
# Date: 29/12/2020
# Release: I
#
# This program save GIGS earthquakes waveform, FFT and spectrogram plots into the images dir. It saves also the data
# The filenames have the form GIGS-AAAA-MM-DDTHHMMSS, the default size plot is 800x250 pixels.
#


from os import environ
import numpy as np
from numpy import save
from numpy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
from obspy import read
import obspy.signal
from obspy.signal.konnoohmachismoothing import konno_ohmachi_smoothing

import datetime

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

def main(): 

    file = "C:\\temp\\2021.txt"
    file1 = "C:\\temp\\notFound.txt"
    image_dir = "C:\\temp\\images\\GIGS\\waveform\\"
    image_dir_FFT = "C:\\temp\\images\\GIGS\\FFT\\"
    image_dir_DATA = "C:\\temp\\images\\GIGS\\DATA\\"
    
    f=open(file,"r")
    lines=f.readlines()
    result=[]
    for x in lines:
        result.append(x.split('|')[1])
    f.close()

    start_date=[]
    start_time=[]

    f1=open(file1,"w")

    for i in range(len(result)):
        start_date.append(result[i].split('T')[0])
        start_time.append(result[i].split('T')[1].split('.')[0])
        start_time_sec = sum(int(i) * 60**index for index, i in enumerate(start_time[i].split(":")[::-1]))
        start_time_sec += 60                                                                                                       # 1 minute
        stop_time = str(datetime.timedelta(seconds=start_time_sec))

        link = "http://webservices.rm.ingv.it/fdsnws/dataselect/1/query?starttime=" + str(start_date[i])+"T"+str(start_time[i])+"&endtime="+str(start_date[i])+"T"+str(stop_time)+"&net=IV&sta=GIGS&cha=HHZ"
        
        try:
            st = read(link)
            
            # Detrend
            # st.detrend()
            # Interpolate
            # st.interpolate(sampling_rate=1/st[0].stats.delta)
            # print(st[0].stats)     # it shows the statistics of the station
            # st[0].data = obspy.signal.filter.highpass(tr.data, 1.0,df=tr.stats.sampling_rate, corners=1, zerophase=True)
        
        except IOError:
            f1.write(link + "\n")
            print("204 HTTP Error: No Content for url at " + str(result[i]))
            continue

        newStartTime = start_time[i].replace(":", "")

        # save the waveform (default size: 800x250 pixels)
        fileName = "GIGS-"+str(start_date[i]) +'T'+ str(newStartTime) 
        st.plot(outfile = image_dir+fileName)  

        # save the row data into a .mseed file
        filename4= "GIGS-"+str(start_date[i]) +'T'+ str(newStartTime)+".mseed"
        st.write(image_dir_DATA+filename4, format="MSEED")

        # FFT with no Smoothing (row), smoothing average, smooting Konno_Ohmachi
        tr =   st[0]
        filename2 =  "GIGS-"+str(start_date[i]) +'T'+ str(newStartTime) + "-FFT"
        #filename5 = "GIGS-"+str(start_date[i]) +'T'+ str(newStartTime) + "-FFTspec"
        #filename6 = "GIGS-"+str(start_date[i]) +'T'+ str(newStartTime) + "-FFTfreqs"
        spec, freqs = rfft(tr.data), rfftfreq(tr.stats.npts, tr.stats.delta)

        # save FFT data
        #save(image_dir+filename5, spec)
        #save(image_dir+filename6, freqs)

        plt.figure(figsize=(12, 6))
        plt.loglog(freqs, np.abs(spec), label="raw", color="grey")
        plt.loglog(freqs, obspy.signal.util.smooth(abs(spec), 5), label="Average")
        plt.loglog(freqs, konno_ohmachi_smoothing(abs(spec), freqs, normalize=True), label="konno ohmachi")

        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Counts")
        plt.legend()
        plt.title("FFT for GIGS "+str(start_date[i]) +'T'+ str(newStartTime))
        plt.savefig(image_dir_FFT+filename2)

         # spectrogram
        #fileName1 = "GIGS-"+str(start_date[i]) +'T'+ str(newStartTime) + "-spettrogram"
        #tr.spectrogram(outfile = image_dir+fileName1, log=True)  

    f1.close()


if (__name__ == "__main__"):
    suppress_qt_warnings()
    main()