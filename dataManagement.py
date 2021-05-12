
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                            D A T A    M A N A G E M E N T                                           #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                Imported libraries                                                   #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                     Functions                                                       #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# 1 - Print all csvFiles contained in a repertory
def printAllCsv(repertoryPath):
   numberOfCsv = 0
   for file in os.listdir(repertoryPath):
       if file.endswith(".csv"):
           print(numberOfCsv," : ", file)
   print("No more.")

# 2 - Calculate number of csv
def csvNumber(repertoryPath):

    csvNumber = 0

    for file in os.listdir(repertoryPath):
        if file.endswith(".csv"):
            csvNumber = csvNumber + 1
    return csvNumber

# 3 - Load all csv data
def getData(repertoryPath): 

    # Loading 90% of data as training data and 10% as testing data
    numberOfTrainingSet = int(csvNumber(repertoryPath) * 0.8)
    
    numberOfCsvLoaded = 0 
    baseTrainingData = pd.DataFrame
    tempTrainingData = pd.DataFrame
    baseTestData = pd.DataFrame
    tempTestData = pd.DataFrame

    for file in os.listdir(repertoryPath):
        
        # Is it a csv ?
        if file.endswith(".csv"):
            
            # Loading in training data
            if numberOfCsvLoaded < numberOfTrainingSet:
                if baseTrainingData.empty:
                    baseTrainingData = pd.read_csv(repertoryPath+ '/' + file)
                else: 
                    tempTrainingData = pd.read_csv(repertoryPath+ '/' + file)
                    baseTrainingData = pd.concat([baseTrainingData, tempTrainingData])
            
            # Loading in testing data
            else:
                if baseTestData.empty:
                    baseTestData = pd.read_csv(repertoryPath+ '/' + file)
                else: 
                    tempTestData = pd.read_csv(repertoryPath+ '/' + file)
                    baseTestData = pd.concat([baseTestData, tempTestData])
            numberOfCsvLoaded = numberOfCsvLoaded + 1
    
    return [baseTrainingData, baseTestData]

# 4 - Calculate the size of a training/testing set
def setSize(repertoryPath):

    valueSetNumber = 0

    for file in os.listdir(repertoryPath):
       if file.endswith(".csv"):
           fileContent = pd.read_csv(repertoryPath+ '/' + file)
           for value in fileContent.index: 
               valueSetNumber = valueSetNumber + 1
       return valueSetNumber

# 5 - Split data into input and output of the neural network
def splitData(repertoryPath, trainingData, testingData):

    print(len(testingData))
    print(len(trainingData))

    numberOfSample = int(csvNumber(repertoryPath))
    sampleSize = setSize(repertoryPath)

    trainingDataSize = int(numberOfSample * 0.8)
    print("TDS : ", trainingDataSize)
    testingDataSize = numberOfSample - trainingDataSize

    #inputTrainingDataSize = int(trainingDataSize * 0.9)
    #inputTestingDataSize = int(testingDataSize * 0.9)
    inputOutputSplit = int(sampleSize * 0.8)

    inputTrainingData = [None] * trainingDataSize
    outputTrainingData = [None] * trainingDataSize
    inputTestingData = [None] * testingDataSize
    outputTestingData = [None] * testingDataSize

    #print("ITrD : ", inputTrainingDataSize)
    #print("OTrD : ", (trainingDataSize - inputTrainingDataSize))
    #print("ITeD : ", inputTestingDataSize)
    #print("OTeD : ", (testingDataSize - inputTestingDataSize))

    print("inputTrainingData : ", inputTrainingData)
    print("outputTrainingData : ", outputTrainingData)
    print("inputTestingData : ", inputTestingData)
    print("outputTestingData : ", outputTestingData)

    for i in range(csvNumber(repertoryPath)):
        if i<trainingDataSize:
            inputTrainingData[i] = trainingData[i*sampleSize:i*sampleSize + inputOutputSplit]
            outputTrainingData[i] = trainingData[i*sampleSize + inputOutputSplit: (i+1) * sampleSize]
            print("InputTrainingData[", i, "] = ", inputTrainingData[i])
            print("OutputTrainingData[", i, "] = ", outputTrainingData[i])
        else:
            j = i-trainingDataSize
            inputTestingData[j] = testingData[j*sampleSize:j*sampleSize + inputOutputSplit]
            outputTestingData[j] = testingData[j*sampleSize + inputOutputSplit: (j+1) * sampleSize]
            print("InputTestingData[", j, "] = ", inputTestingData[j])
            print("OutputTestingData[", j, "] = ", outputTestingData[j])
    
    
    return [[inputTrainingData, outputTrainingData],[inputTestingData, outputTestingData]]

# 6 - Normalize data
def normalize(data):
    normalizer = MinMaxScaler()
    return normalizer.fit_transform(data)

# 7 - Reshape data for neural network
def reshapeData(data):
    for sample in data:
        sample = sample.reshape((1, len(sample), 1))
    return data

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                       E N D                                                         #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
