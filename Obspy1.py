
from obspy import read

import obspy.signal.filter

st = read("C:\\temp\\CONCATENA\\concat08012021.mseed")
tr = st[0]
tr.data = obspy.signal.filter.highpass(tr.data, 1.0,df=tr.stats.sampling_rate, corners=1, zerophase=True)
st.plot()
