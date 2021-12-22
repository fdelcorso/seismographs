# cutErthquakes.py
# Author: FDC
# Date: 07/10/2021, last update 10/12/2021
# Dato un file .mseed in input, viene ricercata la lista dei terremoti occorsi durante lo starttime e l'endtime del file mseed 
# La sintassi del file txt di partenza è #EventID|Time|Latitude|Longitude|Depth/Km|Author|Catalog|Contributor|ContributorID|MagType|Magnitude|MagAuthor|EventLocationName|EventType]
# La lista dei terremoti viene accorciata togliendo quelli di magn < 2 occorsi in un raggio maggiore di circa 100km da Assergi
# Vengono prodotti file .mseed piu' piccoli (uno per ogni slice) e privi di terremoti. Non vengono prodotti quando non ci sono sample nello slice che viene letto.
# Inoltre vengono tagliati quelli al di sotto dei 10K di dimensione
#

from obspy import read
from obspy.core.utcdatetime import UTCDateTime
import numpy as np
from os import environ
from urllib.request import urlopen
import pandas as pd
import datetime
import os


inFile = "GIGS\\24sett-27ott2020-GIGS_HHZ.mseed"
outDir = "GIGS\\HHZ\\"

ch = "HHZ"
sta = "GIGS"
net = "IV"
before_quake = 60       # 1 minuto
after_quake = 900       # 15*60= 15 minuti

lat_GIGS = 42.453167
long_GIGS = 13.572833

long_min = 12.34
long_max = 14.80
lat_min = 41.5
lat_max = 43.35

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


def main():
    start = datetime.datetime.now()
    # Lettura file .mseed in input
    st = read(inFile)
    tr = st[0] 

    # Recupero starttime, endtime del file .mseed
    n_sample = len(st)
    starttime=tr.stats.starttime
    endtime=st[n_sample-1].stats.endtime    # utilizzato nella parte di codice sottostante 

    # Recupero la lista dei terremoti dal sito di INGV da startT a endT e li memorizzo in un file
    # Le righe seguenti sono commentate per evitare di eseguire la query sul sito ogni volta
    # Tolgo il carattere Z finale dalle stringhe di orario
    ### COMMENTATO CODICE PER EVITARE DI FARE PIU' VOLTE LA QUERY AL SITO DI INGV - SCOMMENTARE PER FARSI DARE LA LISTA
    #import requests        
    #startT = str(starttime)[0:-1]
    #endT = str(endtime)[0:-1]
    #url = "https://webservices.ingv.it/fdsnws/event/1/query?starttime=" + str(startT) + "&endtime=" + str(endT) + "&format=text"
    #r = requests.get(url, allow_redirects=True)
    #filename ="listErthquakes" + ".txt"
    #open(filename, 'wb').write(r.content)

    filename ="listErthquakes" + ".txt"

    # Time|Latitude|Longitude|Depth/Km|Magnitude|EventLocationName]
    data = pd.read_table(filename, sep='|', usecols=(1,2,3,4,10,12) )
    df = pd.DataFrame(data=data)
    print("Numero terremoti nel periodo selezionato:",len(df))

    # Dataframe contenente i terremoti da togliere
    quake_to_remove_df = df.loc[ (df['Magnitude'] < 2.0) & ( (df["Latitude"] < lat_min) | 
            (df["Latitude"] > lat_max) ) | (df["Longitude"] < long_min) | (df["Longitude"] > lat_max)]

    # vettore di numpy con i Time dei terremoti da togliere
    time_arr_quake_to_remove = quake_to_remove_df['Time'].to_numpy()

    df = df[~df['Time'].isin(time_arr_quake_to_remove)]
    print("Numero terremoti dopo il taglio:",len(df))     

    # Array di tempi di inizio terremoto (dopo il taglio)
    erthquakesStartTime = df["Time"]

    # inverto l'ordine degli elementi (nella lista sono dal più recente al più vecchio)
    myEarthquakeStartTime = np.flip(erthquakesStartTime.to_numpy())      

    # tolgo 1 minuto prima del terremoto e 15 minuti dopo creando un nuovo file .mseed senza terremoti
    start_time = starttime  
    for j in range(len(myEarthquakeStartTime)):
        
        # nuovo endtime (1 minuto prima dell'inizio terremoto) 
        end_time = UTCDateTime(myEarthquakeStartTime[j]) - before_quake

        # Se due terremoti consecutivi hanno una distanza temporale < 15 min cioè start_time<end_time, non devo fare lo slice
        # Non è corretto fare questo check sul file iniziale dei terremoti, perché non verrebbe tolto il terremoto che viene prima. 
        if (start_time<end_time):

            # slice
            tr1 = tr.slice(starttime=start_time, endtime=end_time) 

            # Se la slice non contiene dati si salta
            if (tr1.stats.npts != 0):
        
                # memorizzazione dello stream in file .mseed
                start_t = str(start_time).replace(":", "")
                end_t = str(end_time).replace(":", "")
                sliceFileName = str(start_t) + "-" + str(end_t) + "." + sta + "_" + ch + ".mseed"
                tr1.write(outDir+sliceFileName, format="MSEED")

                # Se il file .mseed creato è più piccolo di 10Kb va rimosso
                if (os.stat(outDir+sliceFileName).st_size < 10000):
                    os.remove(outDir+sliceFileName)

        # nuovo starttime (15 minuti dopo l'inizio del terremoto)
        start_time = UTCDateTime(myEarthquakeStartTime[j]) + after_quake
        
    end = datetime.datetime.now()
    print(end-start)

if (__name__ == "__main__"):
    suppress_qt_warnings()
    main()