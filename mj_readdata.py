import numpy as np
import matplotlib.pyplot as plt
import pandas
from datetime import datetime

data = pandas.read_csv('Minijets.csv', na_values="-")

# Extract date and time information from string
t =pandas.to_datetime(data.Date, format='%Y-%jT%H:%M:%S.%f')

# Parameters of the system - hardwired in
# Epoch for computing corotating longitudes. Somewhat arbitrary but must be consistent
epoch = pandas.to_datetime('2007-001T12:00:00.000', format='%Y-%jT%H:%M:%S.%f')
# Mean motion of the F ring in deg/day
mmf = 581.96

# Derived minijet properties
# Elapsed seconds between measurment and epoch
secs=(epoch-t).dt.total_seconds()
#Corotating longitude
nl_base = data.Base_Longitude + secs * mmf/24.0/60.0/60.0%360
nl_tip = data.Tip_Longitude + secs * mmf/24.0/60.0/60.0%360
nl_base[nl_base > 360.0] = nl_base-360
nl_tip[nl_tip > 360.0] = nl_tip-360

# Basic plot to show everything worked
plt.plot(nl_base, t, 'ro')
plt.xlim(0, 360)
plt.xlabel(r'$\lambda_n$')
plt.ylabel('Date')
plt.xticks(np.linspace(0, 360, 6, endpoint=True))
plt.savefig('Minijets.pdf')