﻿import sys
from math import *
import random
from matrix import *
#import numpy as np

def collision_detection( x0, y0):
	dist_top = abs(0.0102 * x0 + y0 - 953.72)/ (sqrt(0.0102 **2 + 1**2))
	
	dist_bot = abs(0.0102 * x0 + y0 - 145)/ (sqrt(0.0102 **2 + 1**2))
	dist_left = abs(801 * x0 - 7*y0 - 220835)/ (sqrt(801 **2 + 7**2))
	dist_right = abs(10 * x0 -1363* y0 + 197699)/ (sqrt(10 **2 + 1363**2))
	if dist_top < 40 or dist_bot < 40 or dist_left < 40 or dist_right < 40 :
        #reset: 
		print "Icollsion"
		x = matrix([[0.], [0.], [0.], [0.], [0.], [0.]]) # initial state (location and velocity)
		P = matrix([[1000., 0., 0., 0., 0. ,0.], [0., 1000., 0., 0., 0. ,0.], [0., 0., 1000., 0., 0. ,0.], [0., 0., 0., 1000., 0. ,0.], [0., 0., 0., 0., 1000., 0.], [0., 0., 0., 0., 0., 1000.]]) # initial 
		#TODO: If it happend in last 60: 1) turn 180 2) or calculate angle
		
def measurement_update(P, x, z):
    collision_detection(z[0], z[1])
    Hx = H * x
    zMatrix  = matrix([[z[0]], [z[1]]])
    y = zMatrix - Hx
    S = H * P * matrix.transpose(H) + R
    K = P * matrix.transpose(H) * matrix.inverse(S)
    x = x + (K * y)
    P = (I - K * H) * P
    return P, x

def kalman_filter(x, P):

    lastPrediction = None

    for n in range(len(measurements)):
        
        #TODO Update the filter to support calculating both X and Y and update
        #this line as needed
        z = measurements[n]

        # measurement update
        P, x = measurement_update(P, x, z)

        # prediction
        x = F * x + u
        P = F * P * matrix.transpose(F)

        lastPrediction = [x.value[0][0], x.value[2][0]]
    
    for i in range(60):
        z = lastPrediction

        # measurement update
        P, x = measurement_update(P, x, z)

        # prediction
        x = F * x + u
        P = F * P * matrix.transpose(F)

        #TODO Update to store the last Y prediction as well.
        lastPrediction = [x.value[0][0], x.value[2][0]]
        #TODO This should be changed to append the real Y value.  Right now it
        #is set to duplicate the X value until the filter supports more
        #dimensions
        predictions.append([x.value[0][0], x.value[2][0]])


    return x,P

x = matrix([[0.], [0.], [0.], [0.]]) # initial state (location and velocity)
P = matrix([[10., 0., 0., 0.], [0., 10., 0., 0.], [0., 0., 1000., 0.], [0., 0., 0., 1000.]]) # initial uncertainty
u = matrix([[0.], [0.], [0.], [0.]]) # external motion
F = matrix([[1., 1., 0., 0.], [0., 1., 0., 0.], [0., 0., 1., 1.], [0, 0., 0., 1.]]) # next state function
H = matrix([[1., 0., 0., 0.], [0., 0., 1., 0.]]) # measurement function
R = matrix([[1., 0.], [0., 1.]]) # measurement uncertainty
I = matrix([[1., 0., 0., 0.], [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]]) # identity matrix

filename = sys.argv[1]
#filename = "inputs/test00.txt"
linesOfFile = open(filename, 'r').readlines()
measurements = []
predictions = []

for line in linesOfFile:
    xValue, yValue = line.rstrip('\n').split(',')
    measurements.append([float(xValue), float(yValue)])
#    pass



print(kalman_filter(x, P))

with open('prediction.txt', 'w') as f:
    for prediction in predictions:
        print >> f, '%s,%s' % (int(round(prediction[0],0)),int(round(prediction[1],0)))
    #for prediction in predictions:
     #   print('%s,%s' % (prediction[0], prediction[1]), end="\n", file=f)
    #for _ in range(60):
    #    print >> f, '%s,%s' % (prediction[0].strip(), prediction[1].strip())