#!/usr/bin/env python
# coding: utf-8

# # Jupyter Notebook Draft for Naomi (Project A: Data Augmentation)

# In[2]:


import math
import numpy as np
import random as random
import matplotlib.pyplot as plt
import pandas as pandas
import csv
import collections as collections
from collections import deque
from PIL import Image


# ### Importing CSV Data

# In[3]:


csvList = []
massSpec = []
labelsList = []
USIDList = []
massList = [i for i in range(2001)]
data = pandas.read_csv('DataForNaomi.csv')

def readInCSV(numPlots, sampleType):
    ## reading in CSV file as data base and generating random plot, saving labels
    
    for i in range (numPlots):
        if sampleType == "":
            row = data.sample(1)
        else:
            sampleList = data.loc[(data['sample_label'] == sampleType)]
            row = sampleList.sample(1)
       
        massSpec = row.iloc[:, 1:2002]
        
        labels = row.iloc[:, 2002:2012]
        USID = row.iloc[:, 0]
        
        ## format to list
        massSpec = massSpec.values.tolist()
        massSpec = massSpec[0]
        labels = labels.values.tolist()
        labels = labels[0]
        USID = USID.values.tolist()
        
        ## add to list of lists
        csvList.append(massSpec)
        labelsList.append(labels)
        USIDList.append(USID)
    
    massSpec.append(massSpec)


# ### Averaging Mass Spectra of Same Sample

# In[4]:


def average(sampleType, numSpectraOutput):
    averageWLabel = []
    massSpec1 = []
    massSpec2 = []
    massSpec3 = []
    massSpec4 = []
    massSpec5 = []
    
    readInCSV(5, "CsI")
    massSpec1 = csvList[0][0 : 2001]
    massSpec2 = csvList[1][0 : 2001]
    massSpec3 = csvList[2][0 : 2001]
    massSpec4 = csvList[3][0 : 2001]
    massSpec5 = csvList[4][0 : 2001]
        
    for i in range(numSpectraOutput):
        averageList = []
        averageSpec = []
    
        ## iterates through list of spectra to average, adding every averaged element to final list
        for i in range (2001):
            averageSpec.append((massSpec1[i] + massSpec2[i] + massSpec3[i] + massSpec4[i] + massSpec5[i]) / 5)
            
        ## creating output list with the first spectrum's USID and labels
        averageTemp = USIDList[0] + averageSpec + labelsList[0]
        averageWLabel.append(averageTemp)
        averageList.append(averageSpec)
        counter = 1
        
        ## creating plot
        for tempList in csvList:
            ## Figure
            plt.figure(figsize=(18,8))
            plt.title(f"Random Mass Spectrum of {sampleType} {counter} / {len(csvList)}")
            plt.stem(massList, tempList[0:2001], use_line_collection = True)

            plt.xlabel('m/z')
            plt.ylabel('Intensity')
            plt.show()
            counter += 1
        
        for tempAveList in averageList:
            plt.figure(figsize=(18,8))
            plt.title(f"Mass Spectrum based on Averaging 5 Mass Spectra of {sampleType}")
            plt.stem(massList, tempAveList, use_line_collection = True)

            plt.xlabel('m/z')
            plt.ylabel('Intensity')
            plt.show()
        
    title = f"{numSpectraOutput}Average{sampleType}"
    csvOutput(averageWLabel, title)


# ### Adding random noise

# In[5]:


## creating white noise with a normal distribution
## noiseFactor should be between 0 — 1/10th of basePeak (highest peak)
def gaussianNoise(noiseFactor, numSpectraOutput):
    if noiseFactor < 5 or noiseFactor > 13:
      raise Exception("sorry, but the noiseFactor input must be between 5 and 13")
    
    noiseWLabel = []
    counter = 0
    
    for i in range(numSpectraOutput):
        
        readInCSV(1, "")
        intensityList = csvList[counter][0:2001]
        
        whiteNoiseList = []
        
        basePeak = max(intensityList)
        baseIndex = intensityList.index(basePeak)

        ## creating a sigma to be dependent on both the input noise factor and range of intensities
        mu, sigma = 0, (basePeak / 20) * (noiseFactor / 100 + 1)
        whiteNoise = np.random.normal(mu, sigma, len(intensityList)) * (noiseFactor / 100 + 1)
        whiteNoise = whiteNoise.tolist()

        ## loop through and add original intensity with white noise
        for i in range(len(whiteNoise)):
            whiteNoiseList.append(intensityList[i] + whiteNoise[i])

        ## makes any negative values 0
        for i in range(len(whiteNoiseList)):
            if whiteNoiseList[i] < 0.0:
                whiteNoiseList[i] = 0
        
        noiseTemp = USIDList[0] + whiteNoiseList + labelsList[0]
        noiseWLabel.append(noiseTemp)
        
        ## creating original plot
        plt.figure(figsize=(18,8))
        plt.title("Mass Spectrum")
        plt.stem(massList, intensityList, use_line_collection = True)
        plt.xlabel('m/z')
        plt.ylabel('Intensity')
        plt.show()

        ## creating augmented plot
        plt.figure(figsize=(18,8))
        title = "Random Mass Spectrum with White Noise Factor of {}, mu(mean) of {}, and sigma of {}".format(noiseFactor, mu, sigma)
        plt.title(title)
        plt.stem(massList, whiteNoiseList, use_line_collection = True)
        plt.xlabel('m/z')
        plt.ylabel('Intensity')
        plt.show()
        
        counter += 1
    
    title = f"{numSpectraOutput}GaussianNoiseFactor{noiseFactor}"
    csvOutput(noiseWLabel, title)


# ### Stretch

# In[6]:


def stretch(stretchValue): 
    readInCSV(1, "")
    specList = csvList[0][0:2001]

    basePeak = max(specList)
    baseIndex = specList.index(basePeak)
    startIndex = 0

    ## finding first non-zero value
    for i in range(len(specList)):
        if specList[i] > 0:
            startIndex = i
            break;

    specListReverse = specList.copy()
    specListReverse.reverse()

    ## finding last non-zero value
    for i in range(len(specListReverse)):
        if specListReverse[i] > 0:
            endIndex = i
            break;

    ## creating massList with buckets in new range
    stretchValue = stretchValue / 2
    stretchMassList = [i for i in range((int)(startIndex - stretchValue/2), (int)(endIndex + stretchValue/2))]
    stretchDelta = (stretchMassList[-1] - stretchMassList[0]) / (endIndex - startIndex)

    intensityList = specList.copy()
    intensityList = intensityList[stretchMassList[0] - 1 : stretchMassList[-1]]
    newBaseIndex = intensityList.index(basePeak)
    baseIndexDif = newBaseIndex - baseIndex
    ## intensityList[baseIndex] = basePeak

    finalStretch = []
    for i in stretchMassList:
        finalStretch.append(i * stretchDelta)

    for i in range (len(finalStretch)):
        finalStretch[i] = finalStretch[i] + baseIndexDif

    ## creating massList with buckets the size of the stretchedDelta
    finalStretch = []
    for i in stretchMassList:
        finalStretch.append(i * stretchDelta)
    
    with open(f'Stretch{stretchValue}.csv', 'w', newline = '') as f:
        USID = []
        USID.append('USID')
        label = []
        label.append('Laser_Energy')
        label.append('Laser_Shots')
        label.append('Laser_StdDev')
        label.append('Phase')
        label.append('TIC')
        label.append('Max_Bin_Counts')
        label.append('Charge_Control')
        label.append('mcalDefault')
        label.append('category_label')
        label.append('sample_label')
        CSVStretch = USID + finalStretch + label
        writer = csv.writer(f)
        writer.writerow(CSVStretch)
        writer.writerow(USIDList[0] + intensityList + labelsList[0])
    
    ## Figure
    plt.figure(figsize=(18,8))
    plt.title("Random Mass Spectrum")
    plt.stem(massList[startIndex:endIndex], specList[startIndex:endIndex], use_line_collection = True)
    plt.xlabel('m/z')
    plt.ylabel('Intensity')
    plt.show()

    ## Altered Figure
    plt.figure(figsize=(18,8))
    plt.title("Random Mass Spectrum with Stretch Based on User Input Around Non-Zero Values ")
    plt.stem(finalStretch, intensityList, use_line_collection = True)
    plt.xlabel('m/z')
    plt.ylabel('Intensity')
    plt.show()


# ### Changing intensity

# In[12]:


def intensity(percentageIntensity, numSpectraOutput):
    if percentageIntensity < 6 or percentageIntensity > 13:
      raise Exception("sorry, but the percentageIntensity input must be between 6 and 13")
    
    intensityWLabel = []
    
    for i in range(numSpectraOutput):
        readInCSV(1, "")
        intensityList = csvList[i][0:2001]
        
        mu, sigma = 0, 3.5

        ## finding basePeak and parentPeak (second largest)
        basePeak = max(intensityList)
        intensityTemp = intensityList.copy()
        intensityTemp.remove(basePeak)
        parentPeak = max(intensityTemp)

        augmentedIntensity = []
        for i in range(len(intensityList)):
            randomSign = [-1,1][random.randrange(2)]
            normalFactor = np.random.normal(mu, sigma)
    
            element = (intensityList[i] + (randomSign) * (intensityList[i] * (percentageIntensity / 100))) * normalFactor
            if element < 0:
                element = 0
            augmentedIntensity.append(element)
        
        intensityTemp = USIDList[0] + augmentedIntensity + labelsList[0]
        intensityWLabel.append(intensityTemp)
        
        ## Figure
        plt.figure(figsize=(18,8))
        plt.title("Random Mass Spectrum")
        plt.stem(massList, intensityList, use_line_collection = True)
    
        plt.xlabel('m/z')
        plt.ylabel('Intensity')
        plt.show()


        ## Altered Figure
        plt.figure(figsize=(18,8))
        title = "Random Mass Spectrum with Normal Intensity Distribution and Percentage Intensity of {}, a Mu(mean) of {}, and a Sigma(standard deviation) of {}".format(percentageIntensity, mu, sigma)
        plt.title(title)
        plt.stem(massList, augmentedIntensity, use_line_collection = True)

        plt.xlabel('m/z')
        plt.ylabel('Intensity')
        plt.show()
    
    title = f"{numSpectraOutput}IntensityFactor{percentageIntensity}"
    csvOutput(intensityWLabel, title)


# ### Shift

# In[8]:


def shift(shiftValue):
    if shiftValue < -3 or shiftValue > 3:
      raise Exception("sorry, but the shiftValue input must be between -3 and 3")
    
    readInCSV(1, "")
    intensityList = csvList[0][0:2001]

    mu, sigma = 0, shiftValue
    randomShift = (int)(np.random.normal(mu, sigma))
    massListShift = []

    for i in massList:
        randomShift = (np.random.normal(mu, sigma))
        massListShift.append(i + randomShift)
    
    with open(f'Shift{shiftValue}.csv', 'w', newline = '') as f:
        writer = csv.writer(f)
        USID = []
        USID.append('USID')
        label = []
        label.append('Laser_Energy')
        label.append('Laser_Shots')
        label.append('Laser_StdDev')
        label.append('Phase')
        label.append('TIC')
        label.append('Max_Bin_Counts')
        label.append('Charge_Control')
        label.append('mcalDefault')
        label.append('category_label')
        label.append('sample_label')
        finalShift = USID + massListShift + label
        writer.writerow(finalShift)
        writer.writerow(USIDList[0] + intensityList + labelsList[0])
    
    ## Figure
    plt.figure(figsize=(18,8))
    plt.title("Random Mass Spectrum")
    plt.stem(massList, intensityList, use_line_collection = True)
    plt.xlabel('m/z')
    plt.ylabel('Intensity')
    plt.show()


    ## Altered Figure
    plt.figure(figsize=(18,8))
    plt.title("Random Mass Spectrum with Normal Intensity Distribution and Sigma of " + str(sigma))
    plt.stem(massListShift, intensityList, use_line_collection = True)
    plt.xlabel('m/z')
    plt.ylabel('Intensity')
    plt.show()


# ## CSV File Output

# In[9]:


def csvOutput(augDataWLabel, title):
    with open(f"csv{title}.csv", 'w', newline = '') as f:
        writer = csv.writer(f)
        ## header
        writer.writerow(data.head(1))
        
        ## rest of rows
        for i in range(len(augDataWLabel)):
            writer.writerow(augDataWLabel[i])


# ## Calling of Methods

# In[10]:


csvList = []
average('CsI', 5)


# In[11]:


csvList = []
gaussianNoise(8, 20)


# In[29]:


csvList = []
stretch(26)


# In[13]:


csvList = []
intensity(7, 20)


# In[47]:


csvList = []
shift(3)

