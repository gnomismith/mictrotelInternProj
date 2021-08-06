#!/usr/bin/env python
# coding: utf-8

# ## Imports

# In[1]:


import pandas as pandas
import numpy as np
import csv
import matplotlib.pyplot as plt


# ## Averaging Same Sample_Type and TID

# In[2]:


data = pandas.read_csv('data_projectB_Naomi.csv')

TID = []

## get one TID
for index in range(len(data)):
    TIDValue = str(data.at[index, 'USID'])[0:4]
    TID.append(int(TIDValue))

data['TID'] = TID
## this number should be changed to desired TID
data = data.loc[(data['TID'] == 8110)]

## get one TID and make sure all have the same sample_label; this should be changed to desired sample_label
data = data.loc[(data['sample_label'] == 'CsI')]

## create a list to make a column in data frame for Laser_Energy * Laser_Shots
indexArray = np.arange(len(data))
data = data.reindex(indexArray)

mass1 = data.sample()
mass2 = data.sample()
mass3 = data.sample()
mass4 = data.sample()
mass5 = data.sample()
labels = mass1.iloc[:, 2002:2013]
labels = labels.values.tolist()
labels = labels[0]


mass1 = mass1.iloc[:, 1:2002]
mass1 = mass1.values.tolist()
mass1 = mass1[0]
mass2 = mass2.iloc[:, 1:2002]
mass2 = mass2.values.tolist()
mass2 = mass2[0]
mass3 = mass3.iloc[:, 1:2002]
mass3 = mass3.values.tolist()
mass3 = mass3[0]
mass4 = mass4.iloc[:, 1:2002]
mass4 = mass4.values.tolist()
mass4 = mass4[0]
mass5 = mass5.iloc[:, 1:2002]
mass5 = mass5.values.tolist()
mass5 = mass5[0]

massList = [i for i in range(2001)]
averageSpec = []
    
## iterates through list of spectra to average, adding every averaged element to final list
for i in range (2001):
    averageSpec.append((mass1[i] + mass2[i] + mass3[i] + mass4[i] + mass5[i]) / 5)
            
        
## creating plot
## Figure 1
plt.figure(figsize=(18,8))
plt.title(f"Random Mass Spectrum of 'CsI' 1 / 5")
plt.stem(massList, mass1, use_line_collection = True)

plt.xlabel('m/z')
plt.ylabel('Intensity')
plt.show()

## Figure 2
plt.figure(figsize=(18,8))
plt.title(f"Random Mass Spectrum of 'CsI' 2 / 5")
plt.stem(massList, mass2, use_line_collection = True)

plt.xlabel('m/z')
plt.ylabel('Intensity')
plt.show()

## Figure 3
plt.figure(figsize=(18,8))
plt.title(f"Random Mass Spectrum of 'CsI' 3 / 5")
plt.stem(massList, mass3, use_line_collection = True)

plt.xlabel('m/z')
plt.ylabel('Intensity')
plt.show()

## Figure 4
plt.figure(figsize=(18,8))
plt.title(f"Random Mass Spectrum of 'CsI' 4 / 5")
plt.stem(massList, mass4, use_line_collection = True)

plt.xlabel('m/z')
plt.ylabel('Intensity')
plt.show()

## Figure 5
plt.figure(figsize=(18,8))
plt.title(f"Random Mass Spectrum of 'CsI' 5 / 5")
plt.stem(massList, mass5, use_line_collection = True)

plt.xlabel('m/z')
plt.ylabel('Intensity')
plt.show()

## Averaged Figure
plt.figure(figsize=(18,8))
plt.title(f"Mass Spectrum based on Averaging 5 Mass Spectra of 'CsI'")
plt.stem(massList, averageSpec, use_line_collection = True)

plt.xlabel('m/z')
plt.ylabel('Intensity')
plt.show()

averageSpecLabels = averageSpec + labels

with open("csvAverage5SpecCsITestID8110(20).csv", 'w', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow(data.head(1))
        
    writer.writerow(averageSpecLabels)


# In[ ]:




