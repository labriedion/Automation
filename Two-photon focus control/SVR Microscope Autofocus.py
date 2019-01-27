# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 15:49:06 2017

@author: labeti
"""

#Two-photon autofocus using support vector regression by Étienne Labrie-Dion

import numpy as np
import pandas as pd
from skimage import io
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler


#parameters
squares = 3 #Number of bins per side, total number will be squares^2
stackfile = "stack.tif"
moviefile = "movie.tif"

#Remove background from the stack before loading.
stack = io.imread(stackfile)
stack = np.array(stack)
means = pd.DataFrame()

#Bin the image into squares^2 bins containing the average fluorescence intensity
for z in range(stack.shape[0]):
    oneheight = []
    for x in range(squares):
        xStart = (stack.shape[2] / squares) * x
        xEnd = (stack.shape[2] / squares) * (x+1)        
        for y in range(squares):
            yStart = (stack.shape[1] / squares) * y
            yEnd = (stack.shape[1] / squares) * (y+1)
            oneheight.append(stack[z][yStart:yEnd,xStart:xEnd].mean())
    data = pd.DataFrame(np.asarray(oneheight)).transpose()
    means = means.append(data)

#Prepare the training set (XY) and the Z values to predict (zrange)
XY = np.matrix(means)
zrange = np.arange(stack.shape[0]).reshape(-1,1)

# Scale our data for support vector regression
sc_XY = StandardScaler()
sc_z = StandardScaler()
XY = sc_XY.fit_transform(XY)
zrange = sc_z.fit_transform(zrange)

#Calculate the regression
regressor = SVR(epsilon=.01)
regressor.fit(XY, zrange)

#Open the dataset that we want to predict the Z position from
movie = io.imread(moviefile)
movie = np.array(movie)
means = pd.DataFrame()

#Bin into squares^2 bins with the average fluorescence intensity
for z in range(movie.shape[0]):
    oneheight = []
    for x in range(squares):
        xStart = (movie.shape[2] / squares) * x
        xEnd = (movie.shape[2] / squares) * (x+1)        
        for y in range(squares):
            yStart = (movie.shape[1] / squares) * y
            yEnd = (movie.shape[1] / squares) * (y+1)
            oneheight.append(movie[z][yStart:yEnd,xStart:xEnd].mean())

    data = pd.DataFrame(np.asarray(oneheight)).transpose()
    means = means.append(data)

#Prepare the dataset for prediction
test = np.matrix(means)
test = sc_XY.transform(test)

#Predict the scaled Z position using our regressor
pred = regressor.predict(test)

#Plot the Z position as Z frames
zframes = sc_z.inverse_transform(pred) + 1 #predicted the frames from 0 to stack end -1, so I add 1 to adjust for that
df = pd.DataFrame(zframes)
df.plot()

