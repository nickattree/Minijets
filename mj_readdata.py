import numpy as np
import matplotlib.pyplot as plt
import pandas
from datetime import datetime

data = pandas.read_csv('Minijets.csv', na_values="-")

t =pandas.to_datetime(data.Date, format='%Y-%jT%H:%M:%S.%f')

epoch = 2454102.00
mmf = 581.96

plt.plot(data.Base_Longitude, data.Time, 'ro')
plt.xlim(0, 360)
plt.xlabel(r'$\lambda$')
plt.xticks(np.linspace(0, 360, 6, endpoint=True))
plt.savefig('Minijets.png')