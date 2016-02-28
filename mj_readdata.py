import numpy as np
import pandas
from pandas.tools import plotting
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

data = pandas.read_csv('Minijets.csv', na_values="-")

# Extract date and time information from string
data['t'] =pandas.to_datetime(data.Date, format='%Y-%jT%H:%M:%S.%f')

# Parameters of the system - hardwired in
# Epoch for computing corotating longitudes. Somewhat arbitrary but must be consistent
epoch = pandas.to_datetime('2007-001T12:00:00.000', format='%Y-%jT%H:%M:%S.%f')
# Mean motion and semi-major axis of the F ring in deg/day and km
mmf = 581.96
af = 140221.0

# Derived minijet properties
# Elapsed seconds between measurment and epoch
data['secs']=(epoch-data.t).dt.total_seconds()
# Corotating longitude
nl_base = (data.Base_Longitude + data.secs * mmf/24.0/60.0/60.0) % 360
nl_tip = (data.Tip_Longitude + data.secs * mmf/24.0/60.0/60.0) % 360
nl_base[nl_base > 360.0] = nl_base-360
nl_tip[nl_tip > 360.0] = nl_tip-360
# Lengths and angles
data['r'] = data.Tip_Radius - data.Base_Radius
l = (data.Tip_Longitude - data.Base_Longitude) * af * np.pi / 180.
length = np.sqrt(data.r**2 + l**2)
ratio = data.r/l
data['angle'] = np.arctan(ratio) * 180.0 / np.pi

# pandas plots of exposure vs phase vs time
plt.figure(figsize=(8, 6), dpi=80)
plotting.scatter_matrix(data[['Exposure', 'Phase', 'secs']])
plt.savefig('plot_scatter1.pdf')
# pandas plots of angle vs r
plt.figure(figsize=(8, 6), dpi=80)
temp = data[data.Class=='Classic']
plotting.scatter_matrix(temp[['r', 'angle']])
plt.savefig('plot_scatter2.pdf')

fig, axes = plt.subplots(2, 2, figsize=(8, 6))
# Top left
data.boxplot(column = ['r'], by='Class', ax = axes[0][0])
axes[0][0].set_ylim(-300, 200)
axes[0][0].set_xticklabels([])
axes[0][0].set_xlabel('')
axes[0][0].set_ylabel('(km)')
# Bottom left
data.boxplot(column = ['Exposure'], by='Class', ax = axes[1][0], fontsize =5)
axes[1][0].set_ylim(0, 2000)
axes[1][0].set_ylabel('(ms)')
# Top right
data.boxplot(column = ['Phase'], by='Class', ax = axes[0][1], fontsize =5)
axes[0][1].set_ylim(0, 180)
axes[0][1].tick_params(axis='y', labelleft='off', labelright='on')
axes[0][1].set_ylabel('($^{\circ}$)')
axes[0][1].yaxis.set_label_position("right")
# Bottom right
axes[-1][-1].axis('off')
plt.savefig('plot_box.pdf')

t=data.t
secs=data.secs
# Number of featuers per day over time - TO AUTOMATE
plt.figure(figsize=(8, 6), dpi=80)
# Construct histogram variable, bins as a float and bins labelled as datetimes
bins = np.arange((max(t)-min(t))/np.timedelta64(1, 'D'))
bins_cl = np.arange((max(t[data.Class =='Classic'])-min(t[data.Class =='Classic']))/np.timedelta64(1, 'D'))
bins_bh = np.arange((max(t[data.Class =='Classic - bright head'])-min(t[data.Class =='Classic - bright head']))/np.timedelta64(1, 'D'))
bins_co = np.arange((max(t[data.Class =='Complex'])-min(t[data.Class =='Complex']))/np.timedelta64(1, 'D'))
bins_ob = np.arange((max(t[data.Class =='Extended Object'])-min(t[data.Class =='Extended Object']))/np.timedelta64(1, 'D'))
hist = np.histogram((secs[0]-secs)/24./60./60., bins)[0]
hist_cl = np.histogram((secs[data.Class =='Classic'][6]-secs[data.Class =='Classic'])/24./60./60., bins_cl)[0]
hist_bh = np.histogram((secs[data.Class =='Classic - bright head'][0]-secs[data.Class =='Classic - bright head'])/24./60./60., bins_bh)[0]
hist_co = np.histogram((secs[data.Class =='Complex'][2]-secs[data.Class =='Complex'])/24./60./60., bins_co)[0]
hist_ob = np.histogram((secs[data.Class =='Extended Object'][1]-secs[data.Class =='Extended Object'])/24./60./60., bins_ob)[0]
rng = pandas.date_range(min(t), max(t)-np.timedelta64(1,'D'), freq = 'D')
rng_cl = pandas.date_range(min(t[data.Class =='Classic']), max(t[data.Class =='Classic'])-np.timedelta64(1,'D'), freq = 'D')
rng_bh = pandas.date_range(min(t[data.Class =='Classic - bright head']), max(t[data.Class =='Classic - bright head'])-np.timedelta64(1,'D'), freq = 'D')
rng_co = pandas.date_range(min(t[data.Class =='Complex']), max(t[data.Class =='Complex'])-np.timedelta64(1,'D'), freq = 'D')
rng_ob = pandas.date_range(min(t[data.Class =='Extended Object']), max(t[data.Class =='Extended Object'])-np.timedelta64(1,'D'), freq = 'D')
plt.xlabel('Date')
plt.ylabel('Features')
plt.plot(rng, hist, label = 'Total')
plt.plot(rng_cl, hist_cl, label = 'Classic')
plt.plot(rng_bh, hist_bh, label = 'Classic - bright head')
plt.plot(rng_co, hist_co, label = 'Complex')
plt.plot(rng_ob, hist_ob, label = 'Extended Object')
plt.legend(loc='upper right')
plt.savefig('plot_t.pdf')
