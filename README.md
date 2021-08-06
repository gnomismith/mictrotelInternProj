# mictrotel-Intern-Proj
Data Augmentation for Mass Spectrometry Data from MOMA

## 01.Stretch
stretch(stretchValue); 
Goal: Stretch the data to fit a new range based on the first and last non-zero peak and the stretchValue input by the user, then stretched around the base peak so that the base peak stays still. 
stretchValue:  value to be added to both sides of the new range in order to stretch the data; [7,20] but nothing throws exceptions
Example: stretchValue = 20


## 02. Gaussian Noise
gaussianNoise(noiseFactor, numSpectraOutput)
Goal: Create white noise with a normal distribution of creation from -noiseFactor to +noiseFactor
noiseFactor: the amount of noise desired [5,13]; these are meant to be relative to base peak
Example: noiseFactor = 10 (sigma = 2.333)


## 03. Randomize Intensity
intensity(percentageIntensity, numSpectraOutput); 
Goal: Randomize intensity by randomly adding or subtracting a number normally generated based on the percentageIntensity input by the user.  
percentageInput: multiplied by set of normally generated number
[-percentageInput, percentageInput]; percentageIntensity should be (6, 13)
Example:  percentageIntensity = 7 standard deviation = 3.5 mean = 0


## 04. Shift
shift(shiftValue) 
Goal: Shift peaks left or right based on a an input from a user 
shiftValue: the standard deviation for the normnal generation of the  degree of shift
Example: shiftValue = 3


## 05. Averaging Spectra
average(sampleType, numSpectraOutput);
Goal: create a realistic spectra based on averaging the value of peaks in multiple spectra of the same sample type and TID (test ID)
sampleType: Sample name in the format which it is on the CSV file
Example: sampleType = ‘CsI’


