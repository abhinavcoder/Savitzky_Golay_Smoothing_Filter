# Example Usage:
# python sg.py position.dat 7 2

#  least-squares smoothing method 
import math
import sys

import numpy as np
import numpy.linalg
import pylab as py
import matplotlib.pyplot as plt

def sg_filter(x, m, k=0):
    """
    x = Vector of sample times
    m = Order of the smoothing polynomial
    k = Which derivative
    """
    mid = len(x) / 2        
    a = x - x[mid]
    expa = lambda x: map(lambda i: i**x, a)    
    A = np.r_[map(expa, range(0,m+1))].transpose()
    Ai = np.linalg.pinv(A)

    return Ai[k]

def smooth(x, y, size=5, order=2, deriv=0):

    if deriv > order:
        raise Exception, "deriv must be <= order"

    n = len(x)
    m = size

    result = np.zeros(n)

    for i in xrange(m, n-m):
        start, end = i - m, i + m + 1
        f = sg_filter(x[start:end], order, deriv)
        result[i] = np.dot(f, y[start:end])

    if deriv > 1:
        result *= math.factorial(deriv)

    return result

def plot(t, plots , vel_1 , vel_pos_2):
    n = len(plots)

    for i in range(0,n):
        label, data = plots[i]

        plt = py.subplot(n, 1, i+1)
        plt.tick_params(labelsize=10)
        py.grid()
        py.xlim([t[0], t[-1]])
        py.ylabel(label)

        plt.plot(t, data)
        if i == 0 :
        	plt.plot(t,vel_1)
        	plt.plot(t,vel_pos_2)

    py.xlabel("Time")

def create_figure(size, order):
    fig = py.figure(figsize=(10,10))
    nth = 'th'
    if order < 4:
        nth = ['st','nd','rd','th'][order-1]

    title = "%s point smoothing" % size
    title += ", %d%s degree polynomial" % (order, nth)

    fig.text(.5, .92, title,
             horizontalalignment='center')

def load(name):
    f = open(name)    
    dat = [map(float, x.split(' ')) for x in f]
    f.close()

    pos_1 = [x[0] for x in dat]
    pos_2 = [x[1] for x in dat]
    vel_1 = [x[2] for x in dat]
    t  = [x[3] for x in dat]
    return np.array(pos_1), np.array(pos_2) , np.array(vel_1), np.array(t)

def plot_results(data, size, order):
    pos_1 , pos_2 , vel_1 , t = load(data)
     
    params = (t, pos_1, size, order)
    params_1 = (t, pos_2, size, order)  #this is the velocity parameter from 2nd column data
    vel_pos_2 = smooth(*params_1, deriv=1)  #calculated second velocity
    plots = [
     #   ["Position",     pos_1 ],
        ["Velocity",     smooth(*params, deriv=1)]
      #  ["Acceleration", smooth(*params, deriv=2)]
    ]

    create_figure(size, order)
    plot(t, plots , vel_1 , vel_pos_2)

if __name__ == '__main__':
    data = 'DataNew.txt'
    size =  int(sys.argv[1])
    order = int(sys.argv[2])

    plot_results(data, size, order)
    py.show()