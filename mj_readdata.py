import numpy as np
import matplotlib.pyplot as plt
import pandas

data = pandas.read_csv('Minijets.csv', na_values="-")

# Extract date and time information from string
t =pandas.to_datetime(data.Date, format='%Y-%jT%H:%M:%S.%f')

# Parameters of the system - hardwired in
# Epoch for computing corotating longitudes. Somewhat arbitrary but must be consistent
epoch = pandas.to_datetime('2007-001T12:00:00.000', format='%Y-%jT%H:%M:%S.%f')
# Mean motion and semi-major axis of the F ring in deg/day and km
mmf = 581.96
af = 140221.0

# Derived minijet properties
# Elapsed seconds between measurment and epoch
secs=(epoch-t).dt.total_seconds()
# Corotating longitude
nl_base = data.Base_Longitude + secs * mmf/24.0/60.0/60.0%360
nl_tip = data.Tip_Longitude + secs * mmf/24.0/60.0/60.0%360
nl_base[nl_base > 360.0] = nl_base-360
nl_tip[nl_tip > 360.0] = nl_tip-360
# Lengths and angles
r = data.Tip_Radius - data.Base_Radius
l = (data.Tip_Longitude - data.Base_Longitude) * af * np.pi / 180.
length = np.sqrt(r**2 + l**2)
ratio = r/l
angle = np.arctan(ratio) * 180.0 / np.pi

# Basic plots to show everything worked

# Histogram of the radial sizes of minijets
plt.figure(figsize=(8, 6), dpi=80)
bins = np.arange(-200, 201, 5)
hist = np.histogram(r[data.Class == 'Classic'], bins=bins)[0]
bins = 0.5*(bins[1:] + bins[:-1])
plt.bar(bins, hist, width = 5, fill = False)
plt.xlim(-200, 200)
plt.xlabel('r (km)')
plt.ylabel('Number')
plt.savefig('plot_r.pdf')

# Histogram of the gradients of minijets