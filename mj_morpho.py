# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 10:51:13 2016

@author: noa
"""

# Theoretical time evolution of minijet gradient
def theory(M):
     return np.arctan((1.0 - np.cos(M))/(2.0 * np.sin(M) - 1.5 * M)) * 180.0 / np.pi

# Currently uses graphical comparison method - inefficient and slow
# Also accuracy dependdet on atol parameter chosen but data is not v accurate anyway
# Alternatives are: solving symbolically with sympy solve but this only does linear
# fsolve or Brent method from scipy for single non-linear eqn but this requiers limits a, b with
# f(a,b) of different signs. Func def would have to have extra offset term = -gradient
# and solve repeately between 0<M<1.27, 1.27<M<2pi, 2pi<M<4pi, etc.
# import scipy.optimize
# root = scipy.optimize.brentq(theory, 1.27, 2.0 * np.pi)
# root = scipy.optimize.fsolve(theory,6)
#from sympy import *
#q=solvers.nsolve(((1.0 - cos(M))/(2.0 * sin(M) - 1.5 * M)) + 1.9 , 10)
# Setup graphical comparison method
x = np.arange(0, 251, 0.01) # Roughly every 0.5deg for 40 cycles
y1 = theory(x)
data['rads'] = np.zeros(shape=(len(data)))
data['dela'] = np.zeros(shape=(len(data)))
data['res'] = np.zeros(shape=(len(data)))
# Loop to start here
for i in range(len(data)):
    if np.isnan(data.angle[i]):
        data.rads[i] = np.nan
        data.res[i] = np.nan
        data.dela[i] = np.nan
    else:
        y2 = np.full(len(x), data.angle[i])
        idx = np.argwhere(np.isclose(y1,y2, atol=1.0)).reshape(-1)
        deltaa = data.r[i]/(1.0 - np.cos(x[idx]))
        epi = 2.0 * np.sin(x[idx]) * deltaa
        kep = l[i] - epi
        mkep = -kep / (1.5 * deltaa)
        residual = abs(mkep - x[idx])
        # Select best fit solution
        sol = residual.argmin()
        sol = sol[~np.isnan(sol)]
        data.rads[i] = float(x[idx[sol]])
        data.dela[i] = float(deltaa[sol])
        data.res[i] =  float(residual[sol])

#plt.plot(x, y1)
#plt.plot([0, 20], [data.angle[3], data.angle[3]])
#plt.plot(x[idx], y1[idx], 'ro')
#plt.xlim(0, 20)

data['res'] /= (2.0 * np.pi)
data['cycles'] = data.rads/(2.0 * np.pi)
data['days'] = data.cycles * 0.6196 # Orbital period F ring

# Histogram of the radial sizes of minijets
plt.figure(figsize=(8, 6), dpi=80)
# Cut out unrealistically large solutions for now
temp = data.dela[abs(data.dela)<200]
temp.plot(kind = 'hist', bins =80)
plt.xlabel('$\Delta$a (km)')
plt.ylabel('Features')
plt.xlim(-200, 200)
plt.savefig('plot_dela.pdf')

# Histogram of the angles minijets
plt.figure(figsize=(8, 6), dpi=90)
data.angle[(data.Class=='Classic') | (data.Class=='Classic - bright head')].plot(kind = 'hist', bins =80)
plt.xlabel('Gradient ($^{\circ}$)')
plt.ylabel('Features')
plt.xlim(-90, 90)
plt.savefig('plot_grad.pdf')


"""
# Alternative using numpy
plt.figure(figsize=(8, 6), dpi=80)
bins = np.arange(-200, 201, 5)
hist = np.histogram(r[data.Class == 'Classic'], bins=bins)[0]
bins = 0.5*(bins[1:] + bins[:-1])
plt.bar(bins, hist, width = 5, fill = False)
plt.xlim(-200, 200)
plt.xlabel('r (km)')
plt.ylabel('Features')
plt.savefig('plot_r.pdf')
"""