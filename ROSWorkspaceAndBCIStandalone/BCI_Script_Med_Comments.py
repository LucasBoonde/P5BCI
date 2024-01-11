#!/usr/bin/env python3

"""Denne fil er en kopi af BCI scriptet. Den initierer dog ikke et en ros node, så det vil sige at den kan køres på en normal windows
pc i et python environment. Ideen med dette script er at man kan læse sig igennem hvert step, med lidt mere dybdegående kommentarer"""

"""Den øverste linje i scriptet er en shebang line som bruges af executable scripts i ROS. Med den kan ros se at det er et python
script som initieres."""

import time  # Import the time module
import random
import warnings
import matplotlib.pyplot as plt
import sys
import scipy
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import numpy as np
import moabb
from moabb.datasets import BNCI2014_001
from BCI.msg import BoolStateBCI

#Changes a setting in Numpy so that it does not shorten any matrices printed in the terminal
np.set_printoptions(threshold=sys.maxsize)

#%% --- Setup for MOABB ---
moabb.set_log_level("info")
warnings.filterwarnings("ignore")

#Get the desired Dataset and choose amount of subjects.
dataset = BNCI2014_001()
dataset.subject_list[1]

#%%--- Extracting data from a given dataset ---:

sessions = dataset.get_data(subjects=[1])
subject = 1
session_name = "0train"
run_name = "0"


#Get the raw data from all 22 channels 
raw = sessions[subject][session_name][run_name]



#%%--- Bandpass Filtering---:

#Ved ikke om dette ændrer data senere i for-loopet, eller om man bare bruger raw data igen?

#Cut away frequencies outside of the span of 7 - 30 Hz, let the library choose a filther length and don't introduce a phaseshift
raw.filter(l_freq=7, h_freq=30, filter_length='auto', phase='zero')


#%% --- Separating the data into individual trials ---

"""A session can be divided into runs which can then be separated into trials, each session consists of 12 runs, 
and each run has 48 trial, 12 of each of the 4 classes."""

#Sample rate:
fs = 250

#Seconds pr. trial:
nbSec = 4

#Amount of trial in one run:
nbTrials = 48

#Amount of EEG electrodes
nbChannels = 22

#This matrix will be holding a 2D array for each of the 48 trials (We are only using the EEG channels hence the -4 other channels)
Trials = np.zeros((nbTrials, len(raw.ch_names)-4, nbSec*fs))

#Array for defining the specified stim that has been given to the subject
Class = np.zeros((nbTrials,))

#Array for calculating the Covariance matrix for each trial
Cov = np.zeros((nbTrials, nbChannels, nbChannels))

#Now we want to list the exact samples that corresponds to moments at which a stim was given. We import raw data from the "stim" channel
stim_channel_data = raw.copy().pick_channels(['stim'])

"""This data is stored using the MNE library, so we can try to print(stim_channel_data) which returns  
<RawArray | 1 x 96735 (386.9 s), ~773 kB, data loaded>. This means that stim channel is a very long 1D MNE array of of samples. Each 
sample can have a value between 0-4. A 0 value corresponding to no stim and 1-4 to different types of movement stim given. Furthermore 
we can tell that the samples were taken over a period of 386,9 seconds and the filesize.""" 

#Now we want to extract this MNE array into a standard 1D array. This is stored in the variable stim_channel_values
stim_channel_values = stim_channel_data.get_data()[0]

"""Our goal is now to collect all trials in one large 3D array with the dimensions 22 EEG channels x 1000 samples x Antal Stims. To do this
we are going to use a placeholder array. We used a 2D array with the dimensions 2 x 1000 so that every time we hit a stim, we can collect
the 1000 samples from the 22 EEG channels corresponding to that stim. Then this 2D array is stored in the 3D array and the code
can move on to the next stim sample."""

Arr2D = np.zeros([len(raw.ch_names) - 4, nbSec * fs])

"""OBS: events er basically det samme som stim channel values, så vi gjorde basically det samme to gange, og brugte to forskellige
variabler i for loopet som var samme værdi. Jeg har fjernet evets og vi bruger derfor kun stim_channel_values. Spring derfor ned til næste kommentar.

A smart thing about the MNE arrays is that they can store extra "footnotes" of string to each value in the 1D MNE array. (Kind of).
In this case each stimulus sample has a stored value between 1-4 which indicates which class of stimulus was given. So we use an MNE function
which extracts that information into a 2D array we call events. Basically its a long list of rows with (sample number, 0, class value). We
don't know why there is a 0 in between but is irrelevant. Since the MNE function events_from_annotation besides storing the data in a variable
wants to return it to somewhere as well, we use the underscore "_" to just ignore the otherwise returned data from the function.

events, _ = mne.events_from_annotations(raw)"""


"""This for-loop goes through all the samples for the stim channel,
and jumps inside a for-loop when a stim (value = 3) is given. 
The for-loop extracts 1000 samples of each of the 22 EEG channels, and puts them into a 3D array (Trials), 22x1000x48. 48 for the number of trials. 
In the final part of the loop Values are put into the Class matrix, defining what
stim has been given and Cov matrix that will be used for Common Spatial Pattern"""

"""Now we can start collecting each of the 48 trials. We create a for loop. Since we are only interested in finding samples at the times
a movement stim (values 1-4) was given we define the value 0 as a noStim variable. The for-loop will disregard all the noStim samples. """
noStim = 0 

"""Placeholder variables to keep track of what indexes we are at in the 3D array."""
i = 0  #Keeps track of the 48 stims. The first stim comes 250 samples in, so since we cant take 1000 samples before, we have to take -250 and +750.
x = 0  #Keeps track of the sample number from 0 to 96735


"""We create the 3D array called Trials (48 Trials, 22 channels, 1000 samples) as well as a 1D class aray that stores 48 class values 
to each trial. As we only want to specify between 2 different classes, we take convert stim values 1, 2 and 4 to a single class id 2 and 
take their trial sample values before the stim, meaning it is the same sample values as for noStim."""

for stimSample in stim_channel_values:
    if stimSample != noStim:
        for channel in range(nbChannels):
            currentChannel = raw.ch_names[channel]
            trialData = raw.copy().pick_channels([currentChannel]) #Loads all EEG samples for the specific channel
            if stimSample == 3:
                channelData = trialData.get_data(start=x, stop=x+(nbSec * fs))

            if i == 0:
                channelData = trialData.get_data(start=x-250, stop=x+750)

            else:
                channelData = trialData.get_data(start=x-(nbSec * fs), stop=x)

            Arr2D[channel, :] = channelData
        Trials[i, :, :] = Arr2D
        if stimSample == 3:
            Class[i] = 1
        else:
            Class[i] = 2

        Cov[i, :, :] = np.cov(Arr2D)  #3D array - For each of the 48 trials there is a 22x22 2D array where each element is the covariance between two channels
        i +=1
    x+=1

print("Class Variables", Class)
print("Trials Shape: ", Trials.shape)

print("cov", Cov.shape)




#%% -- LDA Classification -- 

def CSP(C1, C2):
    e, V = scipy.linalg.eig(C1 , C1+C2)
    ind = e.argsort()[::-1]
    e = e[ind]
    V = V[ind]
    Vs = V[:, ind]
    W = np.zeros((2, C1.shape[0]))
    W[0,:] = Vs[:, 0].T
    W[1,:] = Vs[:, -1].T
    return W

def CSP_Features(X, W):
    F = np.zeros((X.shape[0], W.shape[0]))
    for trial in range(X.shape[0]):
        csp_filtered = np.dot(W, np.squeeze(X[trial,:,:]))
        F[trial, :] = np.log(np.var(csp_filtered, axis=1))


    return F


ConfusionMatrix = np.zeros([2,2])
TOL = 0
for test_idx in range(0,nbTrials):
    train_idx = np.ones((48,),dtype=bool)
    train_idx[test_idx] = False
    train_cov = Cov[train_idx, :, :]
    training_class = Class[train_idx]

    W_csp = CSP(np.mean(train_cov[training_class==1,:,:],axis=0), np.mean(train_cov[training_class==2,:,:],axis=0))
    F_csp = CSP_Features(Trials[train_idx,:,:],W_csp)
    #LDA
    lda = LDA().fit(F_csp,training_class)
    test_features = CSP_Features(Trials[test_idx,:,:].reshape((1,22,1000)), W_csp)
    #print("Test Features: ",test_features)
    prediction = lda.predict(test_features)


    #y_pred = lda.predict()
    test_class = Class[test_idx]
    ConfusionMatrix[int(prediction[0])-1,int(test_class)-1] = ConfusionMatrix[int(prediction[0])-1,int(test_class)-1]+1

    score = lda.score(F_csp,training_class)

    print("SCORE: ",score) #Prints the current trainings set's accuracy vs the test set

    

Accuracy = sum(np.diag(ConfusionMatrix))/sum(sum(ConfusionMatrix))
print("Accuracy: ", Accuracy) 




# -- Predicting Random Tral --:

BCIActive = True
ClassifyCount = 0
nrOfNoMovement = 0
nrOfRightMovement=0


while BCIActive==True:
    test_idx = random.randint(0, 48-1)
    train_idx = np.ones((48,), dtype=bool)
    train_idx[test_idx] = False
    train_cov = Cov[train_idx, :, :]
    training_class = Class[train_idx]

    W_csp = CSP(np.mean(train_cov[training_class == 1, :, :], axis=0),
                np.mean(train_cov[training_class == 2, :, :], axis=0))
    F_csp = CSP_Features(Trials[train_idx, :, :], W_csp)

    # LDA
    lda = LDA().fit(F_csp, training_class)
    test_features = CSP_Features(Trials[test_idx, :, :].reshape((1, 22, 1000)), W_csp)

    #Predict the current Class:
    prediction = lda.predict(test_features)
    print("Prediction: ", prediction)
    if prediction == int(1):
        print("Classifier Has Predicted a Movement")
        actual_class = Class[test_idx]
        print("Actual Class: ", actual_class)
        # Send The confirm action to the robot.
        nrOfRightMovement += 1
        BCIActive = False

    else:
        print("You seem to be idle")
        nrOfNoMovement += 1
    ClassifyCount +=1


    print("Test Index:" , test_idx)
    print("Classifying loop nr: ", ClassifyCount)
    print("No movements detected: ", nrOfNoMovement)
    print("Right Hand Movement Classified", nrOfRightMovement)
