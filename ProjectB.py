#!/usr/bin/env python
# coding: utf-8

# ## References

# #### take one TID, normalize based on highest peak so they are all relative to one another, sort by phase and then laser shot times laser energy

# ## Imports

# In[11]:


import math
import csv
import matplotlib.pyplot as plt
import pandas as pandas
from sklearn import preprocessing
import numpy as np
from PIL import Image


# ## Intensity Image

# In[24]:


data = pandas.read_csv('data_projectB_Naomi.csv')

TID = []

## get one TID
for index in range(len(data)):
    TIDValue = str(data.at[index, 'USID'])[0:4]
    TID.append(int(TIDValue))

data['TID'] = TID
## this number should be changed to desired TID
data = data.loc[(data['TID'] == 8111)]

## get one TID and make sure all have the same sample_label; this should be changed to desired sample_label
data = data.loc[(data['sample_label'] == 'CsI')]
laserStrength = []

## create a list to make a column in data frame for Laser_Energy * Laser_Shots
indexArray = np.arange(len(data))
data = data.reindex(indexArray)
for index in range(len(data)):
    laserStrength.append(data.at[index, 'Laser_Energy'] * data.at[index, 'Laser_Shots'])

## add column to dataframe
data['Laser_Strength'] = laserStrength

## create three differet dataframes separated by phases, sort by Laser_Strength
phase1Data = data.loc[(data['Phase'] == 1)]
phase1Data = phase1Data.sort_values(by = ['Laser_Strength'])
phase2Data = data.loc[(data['Phase'] == 2)]
phase2Data = phase2Data.sort_values(by = ['Laser_Strength'])
phase3Data = data.loc[(data['Phase'] == 3)]
phase3Data = phase3Data.sort_values(by = ['Laser_Strength'])
phaseData = []
phaseData.append(phase1Data)
phaseData.append(phase2Data)
phaseData.append(phase3Data)

orderedData = pandas.concat(phaseData, ignore_index = True)

massSpec = data.iloc[:, 1:2002]
dataArray = massSpec.to_numpy()
print(orderedData)
# normalizedData = preprocessing.normalize(dataArray) ## can change norm to l1(have row sum = 0) or max(values will be rescaled by the maximum of the absolute values)

## normalixing data based on 255
rowCounter = -1

for row in normalizedData:
    rowCounter += 1
    Max = row.max()
    Min = row.min()
    for j in range (len(row)):
        normalizedData[rowCounter][j] = normalizedData[rowCounter][j] *(255/(Max-Min))
        
img = Image.fromarray(np.uint8(normalizedData * 255) , 'L')
img.save("2dDataImage(1).png")
img.show()

