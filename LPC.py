#!usr/bin/python
import numpy as np

class LPC_computing:
    def __init__(self,hammingFrames):
        self.hammingFrames=hammingFrames



def autocorrelation(hammingFrames):
    correlateFrames = []
    for k in range(len(hammingFrames)):
        correlateFrames.append(np.correlate(hammingFrames[k], hammingFrames[k], mode='full'))
    # print 'Each frame after windowing and autocorrelation: \n',correlateFrames
    yolo = correlateFrames[len(correlateFrames) / 2:]
    return yolo


def levinsonDurbin(correlateFrames):
    # normalizedCF = preprocessing.normalize(correlateFrames, norm='l2')
    filt1 = levinson_durbin(correlateFrames, 13)
    print (filt1.numerator[1:])


def myLPC():
    folder = input('Give the name of the folder that you want to read data: ')
    amount = input('Give the number of samples in the specific folder: ')
    for x in range(1, int(amount) + 1):
        wav = '/' + folder + '/' + str(x) + '.wav'
        print (wav)
        emphasizedSignal, signal, rate = preEmphasis(wav)
        # visualize(rate,signal)
        frames, frameSize = framing(rate, signal)
        hammingFrames = hamming(frames, frameSize)
        correlateFrames = autocorrelation(hammingFrames)
        merged = correlateFrames[0]
        for x in range(1, len(correlateFrames) - 1):
            merged = np.append(merged, correlateFrames[x])
        lev_Dur = levinsonDurbin(merged)


def LPC_autocorrelation(order=13):
    # Takes in a signal and determines lpc coefficients(through autocorrelation method) and gain for inverse filter.
    folder = input('Give the name of the folder that you want to read data: ')
    amount = input('Give the number of samples in the specific folder: ')
    for x in range(1, int(amount) + 1):
        wav = '/' + folder + '/' + str(x) + '.wav'
        print (wav)
        # preemhasis filter
        emphasizedSignal, signal, rate = preEmphasis(wav)
        length = emphasizedSignal.size
        # prepare the signal for autocorrelation , fast Fourier transform method
        autocorrelation = sig.fftconvolve(emphasizedSignal, emphasizedSignal[::-1])
        # autocorrelation method
        autocorr_coefficients = autocorrelation[autocorrelation.size / 2:][:(order + 1)]

        # using levinson_durbin method instead of solving toeplitz
        lpc_coefficients_levinson = levinson_durbin(autocorr_coefficients, 13)
        print ('With levinson_durbin instead of toeplitz ', lpc_coefficients_levinson.numerator)

        # The Toeplitz matrix has constant diagonals, with c as its first column and r as its first row. If r is not given
        R = linalg.toeplitz(autocorr_coefficients[:order])
        # Given a square matrix a, return the matrix ainv satisfying
        lpc_coefficients = np.dot(linalg.inv(R), autocorr_coefficients[1:order + 1])
        # (Multiplicative) inverse of the matrix (inv),  Returns the dot product of a and b. If a and b are both scalars
        # or both 1-D arrays then a scalar is returned; otherwise an array is returned. If out is given, then it is returned  (np.dot())
        lpc_features = []
        for x in lpc_coefficients:
            lpc_features.append(x)
        print (lpc_features)


def LPC():
    folder = input('Give the name of the folder that you want to read data: ')
    amount = input('Give the number of samples in the specific folder: ')
    for x in range(1, int(amount) + 1):
        wav = '/' + folder + '/' + str(x) + '.wav'
        print (wav)
        emphasizedSignal, signal, rate = preEmphasis(wav)
        filt = lpc(emphasizedSignal, order=13)
        lpc_features = filt.numerator[1:]
        print (len(lpc_features))
        print (lpc_features)


def main():
    LPC()
    # myLPC()
    LPC_autocorrelation()


main()