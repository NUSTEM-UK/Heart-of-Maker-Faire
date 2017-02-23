"""Generate heartbeat data amplitudes.

Based on work in http://stackoverflow.com/questions/4387878/
by Diarmaid O Cualain and Steve Tjoa.
Published here: https://github.com/diarmaidocualain/ecg_simulation
Licensed under BSD, more-or-less.
Modifications by Jonathan Sanderson, Northumbria University, 2017-01-31
"""

import pylab
import scipy
import scipy.signal as signal
import numpy

print('Simulating heart ecg')

# The "Daubechies" wavelet is a rough approximation to a real,
# single, heart beat ("pqrst") signal
# Ref: https://en.wikipedia.org/wiki/Daubechies_wavelet
# Ref: https://en.wikipedia.org/wiki/Ingrid_Daubechies

fs = 8000.0

pqrst = signal.wavelets.daub(10)

# Add the gap after the pqrst when the heart is resting.
samples_rest = 10
zero_array = numpy.zeros(samples_rest, dtype=float)
pqrst_full = numpy.concatenate([pqrst, zero_array])

t = scipy.arange(len(pqrst_full))/fs

pylab.plot(t, pqrst_full)
pylab.show()
