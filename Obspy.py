from obspy import read, UTCDateTime
#from obspy.clients.arclink.client import Client

import numpy as np
import matplotlib.pyplot as plt

# %%
## TODO:
# 1. ciclo for per gli spettrogrammi sui 3 canali
# 2. salvataggio su file degli spettrogrammi
# 3. 

# Data are coming from the web site webservices.rm.ingv.it , Network: IV, station: GIGS, channels: HHZ, HHN, HHE

# Terremoto del 22 marzo 2020 ore 6.01:20 (UTC), 07:01:20 (UTC + 1 for Italy) epicentro SLOVENIA-CROAZIA magnitudo 4.9
# http://terremoti.ingv.it/en/events?starttime=2020-03-22+00%3A00%3A00&endtime=2020-03-22+23%3A59%3A59&last_nd=-1&minmag=2&maxmag=10&mindepth=-10&maxdepth=1000&minlat=35&maxlat=49&minlon=5&maxlon=20&minversion=100&limit=30&orderby=ot-desc&tdmt_flag=-1&lat=0&lon=0&maxradiuskm=-1&wheretype=area&box_search=Italia

link = "http://webservices.rm.ingv.it/fdsnws/dataselect/1/query?starttime=2020-03-22T06:00:00&endtime=2020-03-22T06:26:0&net=IV&sta=GIGS"
st = read(link)
# print(st)             # it shows the Traces in Stream
#print(st[0].stats)     # it shows the statistics of the station
st.plot(color='gray', tick_format='%I:%M %p', starttime=st[0].stats.starttime, endtime=st[0].stats.endtime)

# Channel HHZ:
link = "http://webservices.rm.ingv.it/fdsnws/dataselect/1/query?starttime=2020-03-22T06:00:00&endtime=2020-03-22T06:26:0&net=IV&sta=GIGS&cha=HHZ"
st = read(link)
st[0].spectrogram(log=True)

# Channel HHN:
link = "http://webservices.rm.ingv.it/fdsnws/dataselect/1/query?starttime=2020-03-22T06:00:00&endtime=2020-03-22T06:26:0&net=IV&sta=GIGS&cha=HHN"
st = read(link)
#st.plot(color='gray', tick_format='%I:%M %p', starttime=st[0].stats.starttime, endtime=st[0].stats.endtime)
st[0].spectrogram(log=True) 

# Channel HHE:
link = "http://webservices.rm.ingv.it/fdsnws/dataselect/1/query?starttime=2020-03-22T06:00:00&endtime=2020-03-22T06:26:0&net=IV&sta=GIGS&cha=HHE"
st = read(link)
#st.plot(color='gray', tick_format='%I:%M %p', starttime=st[0].stats.starttime, endtime=st[0].stats.endtime)
st[0].spectrogram(log=True) 

# Terremoto del 22 marzo 2020 ore 5.24:03 (UTC), 06:24:03 for  Italy (UTC + 1) epicentro SLOVENIA-CROAZIA magnitudo 5.1
# http://terremoti.ingv.it/en/events?starttime=2020-03-22+00%3A00%3A00&endtime=2020-03-22+23%3A59%3A59&last_nd=-1&minmag=2&maxmag=10&mindepth=-10&maxdepth=1000&minlat=35&maxlat=49&minlon=5&maxlon=20&minversion=100&limit=30&orderby=ot-desc&tdmt_flag=-1&lat=0&lon=0&maxradiuskm=-1&wheretype=area&box_search=Italia

link = "http://webservices.rm.ingv.it/fdsnws/dataselect/1/query?starttime=2020-03-22T05:20:00&endtime=2020-03-22T05:46:0&net=IV&sta=GIGS"
st = read(link)
st.plot(color='gray', tick_format='%I:%M %p', starttime=st[0].stats.starttime, endtime=st[0].stats.endtime)

# channel HHZ:
st[0].spectrogram(log=True)
link = "http://webservices.rm.ingv.it/fdsnws/dataselect/1/query?starttime=2020-03-22T05:20:00&endtime=2020-03-22T05:46:0&net=IV&sta=GIGS&cha=HHZ"
st = read(link)
st[0].spectrogram(log=True) 

# Channel HHN:
link = "http://webservices.rm.ingv.it/fdsnws/dataselect/1/query?starttime=2020-03-22T05:20:00&endtime=2020-03-22T05:46:0&net=IV&sta=GIGS&cha=HHN"
st = read(link)
st[0].spectrogram(log=True) 

# Channel HHE:
link = "http://webservices.rm.ingv.it/fdsnws/dataselect/1/query?starttime=2020-03-22T05:20:00&endtime=2020-03-22T05:46:0&net=IV&sta=GIGS&cha=HHE"
st = read(link)
st[0].spectrogram(log=True) 

# %%
# Data are coming from the CUORE seismo1 seismometer 

from obspy import read
import os

cwd = os.getcwd()
print(cwd)

mydir = "seismo1/"
for files in os.listdir(mydir):
    for file in files:
        st = read(file)
        print(st[0].stats) 
    #st.plot(color='gray', tick_format='%I:%M %p', starttime=st[0].stats.starttime, endtime=st[0].stats.starttime)
    #tr = st[0]
    #st[0].spectrogram(log=True)

# print(tr.stats)                    # OK
# print(len(tr))                     # OK

#st.plot(color='gray', tick_format='%I:%M %p', starttime=st[0].stats.starttime, endtime=st[0].stats.starttime)




# %%
