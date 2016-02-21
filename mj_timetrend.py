# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 11:13:28 2016

@author: noa
"""

import datetime

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
start = pandas.to_datetime(seriesdata.Start_Time.str[0:4] + '-' + seriesdata.Start_Time.str[4:7], format = '%Y-%j')
start = start + fracdays
stop = pandas.to_datetime(seriesdata.Stop_Time.str[0:4] + '-' + seriesdata.Stop_Time.str[4:7], format = '%Y-%j')
stop = stop + fracdays2

# Location of all the features in space and time
# Need to fix round the end erros where Startlong<360<Stoplong
plt.figure(figsize=(8, 6), dpi=80)
plt.plot([seriesdata.Start_Longitude,seriesdata.Stop_Longitude],[start,stop], color = 'Black')
plt.plot(nl_base, t, 'ro')
plt.xlim(0, 360)
plt.xlabel(r'$\lambda_n$ ($^{\circ}$)')
plt.ylabel('Date')
plt.xticks(np.linspace(0, 360, 5, endpoint=True))
plt.savefig('plot_coverage.pdf')

# Histogram of the number of features per sequence

# Features persequence over time

# Number of features relative to Prometheus
