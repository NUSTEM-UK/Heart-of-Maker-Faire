# Based on http://stackoverflow.com/questions/4387878/simulator-of-realistic-ecg-signal-from-rr-data-for-matlab-or-python


import pylab
import scipy
import scipy.signal as sig
import numpy
# rr = [1.0, 1.0, 0.5, 1.5, 1.0, 1.0] # rr time in seconds
rr = [1.0]
samples = 240  # number of samples
# Resample data to smooth output
pqrst = sig.wavelets.daub(10) # just to simulate a signal, whatever
samples_rest = 10
zero_array = numpy.zeros(samples_rest, dtype=float)
pqrst_full = numpy.concatenate([pqrst, zero_array])

ecg = sig.resample(pqrst_full, int(samples))

pylab.plot(ecg)
pylab.show()

print ecg
