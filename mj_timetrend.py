# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 11:13:28 2016

@author: noa
"""

from datetime import datetime

seriesdata = pandas.read_csv('Series.csv', na_values="-")
seriesdata.Start_Time=seriesdata.Start_Time.astype(str)
seriesdata.Stop_Time=seriesdata.Stop_Time.astype(str)

# Extract datetimes from strangely formatted strings
# Fracdays is needed to deal with fractional amounts of days. TO BE CLEANED UP
fracdays = seriesdata.Start_Time.str[7:].astype(float)
fracdays = pandas.to_timedelta(fracdays, 'D')
fracdays2 = seriesdata.Stop_Time.str[7:].astype(float)
fracdays2 = pandas.to_timedelta(fracdays2, 'D')
# slices up string and date converts each bit
seriesdata['start'] = pandas.to_datetime(seriesdata.Start_Time.str[0:4] + '-' + seriesdata.Start_Time.str[4:7], format = '%Y-%j')
seriesdata['start'] = seriesdata['start'] + fracdays
seriesdata['stop'] = pandas.to_datetime(seriesdata.Stop_Time.str[0:4] + '-' + seriesdata.Stop_Time.str[4:7], format = '%Y-%j')
seriesdata['stop'] = seriesdata['stop'] + fracdays2

# Location of all the features in space and time
# Need to fix round the end erros where Startlong<360<Stoplong
plt.figure(figsize=(8, 6), dpi=80)
plt.plot([seriesdata.Start_Longitude,seriesdata.Stop_Longitude],[seriesdata.start,seriesdata.stop], color = 'Black')
plt.plot(nl_base, t, 'ro')
plt.xlim(0, 360)
plt.xlabel(r'$\lambda_n$ ($^{\circ}$)')
plt.ylabel('Date')
plt.xticks(np.linspace(0, 360, 5, endpoint=True))
plt.savefig('plot_coverage.pdf')

# count features per sequence and adjust for longitude coverage
# Can probably be done better with groupby
# Ignores last one whichis a NAN for somereason - need to check this!
series,count = np.unique(data.Observation, return_counts = True)
seriesdata['counts'] = pandas.Series(count[:-1])
seriesdata['adjcount'] = 360.*seriesdata.counts/seriesdata.Coverage
# Histogram of the number of features per sequence
plt.figure(figsize=(8, 6), dpi=80)
seriesdata.adjcount.where(seriesdata.Coverage > 50.).plot(kind='hist', bins = 40)
plt.xlabel('Adjusted Features')
plt.ylabel('Number of Sequences')
plt.savefig('plot_featuresperseq.pdf')

# Features persequence over time
plt.figure(figsize=(8, 6), dpi=80)
fig, ax = plt.subplots(1,1)
# This is how to format dates for plotting in matplotlib
# Convert pandas -> datatime.datetime -> seconds past epoch with date2num
seriesdata['plotstart'] = matplotlib.dates.date2num(seriesdata.start.astype(datetime))
plt.scatter(seriesdata.plotstart[seriesdata.Coverage > 50.], seriesdata.adjcount[seriesdata.Coverage > 50.], c=seriesdata.Coverage[seriesdata.Coverage > 50.])
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y'))
plt.xlabel('Date')
plt.ylabel('Adjusted Features')
plt.ylim(0, 75)
plt.plot([733742.0,733742.0],[0,75], linestyle ='--')
plt.annotate('Prometheus Closest Approach', xy=(733800.0, 70), rotation = 90, fontsize = 6)
cb = plt.colorbar(shrink =0.5)
cb.set_label('Coverage ($^{\circ}$)')
plt.savefig('plot_timetrend.pdf')

# Number of features relative to Prometheus
# Prometheus orbital parameters
prom_mlepoch = 306.117
prom_epoch = pandas.to_datetime('2004-001T00:00:00.000', format='%Y-%jT%H:%M:%S.%f')
prom_mm = 587.2852370
l_prom = (prom_mlepoch + (prom_epoch-data.t).dt.total_seconds()*(prom_mm/24.0/60.0/60.)) % 360.00	#Actually mean longitude (no ecc)
data['rel'] = data.Base_Longitude - l_prom
data.rel[data.rel>180.0]= -1.*(l_prom[data.rel>180.0]+360.0-data.Base_Longitude[data.rel>180.0])
data.rel[data.rel<-180.0]= data.Base_Longitude[data.rel<-180.0]+360.0-l_prom[data.rel<-180.0]
plt.figure(figsize=(8, 6), dpi=80)
data.rel.plot(kind = 'hist', bins = 72)
plt.xlim(-180, 180)
plt.xlabel(r'$\lambda$-$\lambda_{Prom}$ ($^{\circ}$)')
plt.ylabel('Features')
plt.savefig('plot_reltoprom.pdf')

# Fourier Transforms 
# Will do these properlly by interpolating onto regular spacing later
# Some longitudes are Nans - get rid of hem for now
y1 = data.Base_Longitude[~np.isnan(data.Base_Longitude)]
y2 = data.rel[~np.isnan(data.rel)]
bins = np.arange(0, 360)
y1 = np.histogram(y1, bins = bins)[0]
y2 = np.histogram(y2, bins = bins)[0]
fft_rel = np.fft.rfft(y1)
fft_base = np.fft.rfft(y2)
x = np.arange(fft_rel.size)
x = 360./x
# Plot Power spectrum (abs(fft)^2) against xth longitude bin
plt.figure(figsize=(8, 6), dpi=80)
plt.loglog(x, abs(fft_base)**2.0, label = r'$\lambda_n$')
plt.loglog(x, abs(fft_rel)**2.0, label = r'$\lambda$-$\lambda_{Prom}$')
plt.legend(loc='upper left')
plt.ylabel('Power')
plt.xlabel('($^{\circ}$)')
plt.savefig('plot_fft.pdf')