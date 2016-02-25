# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 10:51:13 2016

@author: noa
"""

# Basic plots to show everything worked
# Histogram of the radial sizes of minijets
plt.figure(figsize=(8, 6), dpi=80)
bins = np.arange(-200, 201, 5)
hist = np.histogram(r[data.Class == 'Classic'], bins=bins)[0]
bins = 0.5*(bins[1:] + bins[:-1])
plt.bar(bins, hist, width = 5, fill = False)
plt.xlim(-200, 200)
plt.xlabel('r (km)')
plt.ylabel('Features')
plt.savefig('plot_r.pdf')

# Alterative usin gpandas
data.r[data.Class=='Classic'].plot(kind = 'hist', bins =80)