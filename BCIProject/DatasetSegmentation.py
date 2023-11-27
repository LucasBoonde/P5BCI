import warnings

import matplotlib.pyplot as plt
import sys
import mne
import pandas as pd
from scipy.signal import filtfilt
from scipy import stats
import scipy
import seaborn as sns
from mne.decoding import CSP
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.pipeline import make_pipeline
import numpy as np

import moabb
from moabb.datasets import BNCI2014_001
from moabb.evaluations import WithinSessionEvaluation
from moabb.paradigms import LeftRightImagery

#Just prints the whole array instead of [x, y, ... , x, y]
np.set_printoptions(threshold=sys.maxsize)


#%% --- Setup for MOABB ---
moabb.set_log_level("info")
warnings.filterwarnings("ignore")

#Get the desired Dataset and choose amount of subjects.
dataset = BNCI2014_001()
dataset.subject_list[1]


#GENERAL INFORMATION FOR THE DATASET WE ARE USING
#Number of Subjects = 10
#Number of Channels = 22 + 3 EOG
#Number og Classes = 4(rh, lh, feet, tongue)
#Trials/Class = 144
#Trials Length = 4sec
#Sampling Rate = 250Hz
#Sessions = 2

#%%--- Extracting data from a given dataset ---:

sessions = dataset.get_data(subjects=[1])
subject = 1
session_name = "0train"
run_name = "0"


#Get the raw data from all 22 channels and plots them
raw = sessions[subject][session_name][run_name]
raw.plot(n_channels=len(raw.ch_names), title='EEG data - Subject {}, Session {}, Run {}'.format(subject, session_name, run_name))
plt.show()


#%%--- Bandpass Filtering---:

#Ved ikke om dette ændrer data senere i for-loopet, eller om man bare bruger raw data igen?
raw.filter(l_freq=0.5, h_freq=30, filter_length='auto', phase='zero')
raw.plot(n_channels=len(raw.ch_names), title='EEG data - After Bandpass Filter')

plt.show()


#%% --- Extracting Individual Trials ---
"""Hver session har flere runs, og vi kan inddele dem i trials, 
så vi senere kan predicte om det er en action eller ej"""

"""A session can be divided into runs, and trials, each session consists of 12 runs, 
and each run has 48 trial, 12 of each of the 4 classes."""

#Sample rate:
fs = 250
#Seconds pr. trial:
nbSec = 4
#Samples pr. trial:
TrialDuration = fs*nbSec
#Amount of trial in one run:
nbTrials = 48
#Total amount of seconds for one run
nbSecs = 385
nbElectrodes = 22
nbSubjects = 10

#Trials pr class pr run = 12
#Total amount of runs = 12

#This matrix will be holding a 2D array for each of the 48 trials
#len(raw.ch_names)-4 fordi vi kun bruger EEG Channels, men kan ændres senere.
Trials = np.zeros((nbTrials, len(raw.ch_names)-4, nbSec*fs))
#Defines what stim has been given to the subject
Class = np.zeros((nbTrials,))


Cov = np.zeros((nbTrials, nbElectrodes, nbElectrodes))


#Selects the Stim channel
stim_channel_data = raw.copy().pick_channels(['stim'])

# Extract the values from the 'stim' channel
stim_channel_values = stim_channel_data.get_data()[0]

threshold = 0
i = 0
x = 0
z = 0

#Creates a Numpy 2D array. 22x1000. 22 because of the EEG channels and 1000 is the samples extracted for each trial.
Arr2D = np.zeros([len(raw.ch_names) - 4, nbSec * fs])

#Checks when and what stim is given to the suspect
events, _ = mne.events_from_annotations(raw)

"""This for-loop goes through all the samples for the stim channel,
and jumps to the inside for-loop when a stim is given. 
inside that loop it extracts 1000 samples of each of the 
EEG channels, and puts them into a 3D array (Trials), 22x1000x48.
In the final part of the loop Values are put into the Class matrix, defining what
stim has been given and Cov matrix that will be used for Common Spatial Pattern"""

for y in stim_channel_values:
    if y != threshold:
        for z in range(nbElectrodes):
            currentChannel = raw.ch_names[z]
            trialData = raw.copy().pick_channels([currentChannel])
            channelData = trialData.get_data(start=x, stop=x+(nbSec * fs))
            Arr2D[z, :] = channelData
        event_sample = events[i]
        stim_value = raw.copy().pick_channels(['stim']).get_data()[0][event_sample]
        Trials[i, :, :] = Arr2D
        if stim_value[0] == 1:
            Class[i] = stim_value[0]
        else:
            Class[i] = 2

        Cov[i, :, :] = np.cov(Arr2D)
        i +=1
    x+=1

#print("COVARIANCE MATRIX SHAPE", Cov)
print("Arr2D Shape", Arr2D.shape)

#%% --- COMMON SPATIAL PATTERN (CSP) ---

C_right = np.mean(Cov[Class == 1, :, :], axis=0)
C_none = np.mean(Cov[Class == 2, :, :], axis=0)
C_combined = C_right + C_none

e, V = scipy.linalg.eig(C_right, C_combined)
#print("eigen Vector: ", V)
#print("eigenvalue: ", e)
ind = e.argsort()[::-1]
e = e[ind]
V = V[ind]
Vs = V[:, ind]
W_Right = Vs[:, 0]
W_None = Vs[:, -1]

#%% -- Plot CSP Features --



fig, ax = plt.subplots()
lr_idx = np.any([Class == 1])
LR_trials = Trials[lr_idx, :, :]


trial = np.squeeze(LR_trials)
right_feature = np.var(np.dot(W_Right, trial), axis=1)
none_feature = np.var(np.dot(W_None, trial), axis=1)
print("LR_Trials Shape: ", LR_trials.shape)
colors = Class

plt.scatter(np.log(right_feature), np.log(none_feature), s=100, c=colors, cmap='bwr_r')

ax.set(xlabel='log(var(w_1 X))', ylabel='log(var(w_2 X))')
plt.show()

#%% -- LDA Classification --
def CSP(C1, C2):
    print("C1", C1.shape)
    print("C2", C2.shape)
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
        csp_filtered = np.dot(W , np.squeeze(X[trial, :, :]))
        F[trial, :] = np.log(np.var(csp_filtered, axis=1, ddof=0))
    return F


lr_idx = np.any([Class == 1, Class == 2])
LR_trials = Trials[lr_idx, :, :].reshape((48,22,1000))
print("LR_trials: ", LR_trials.shape)
LR_class = Class[lr_idx].reshape((48,))
print("LR Class: ", LR_class.shape)
LR_CovMat = Cov[lr_idx, :, :].reshape((48,22,22))
print("LR Cov", LR_CovMat.shape)

N = LR_trials.shape[1]
#print("N Size: ", N)

ConfusionMatrix = np.zeros([2,2])

for test_idx in range(1,N):
    train_idx = np.ones((48,),dtype=bool)#(range(1, test_idx-1)) + list(range(test_idx + 1, N))
    train_idx[test_idx] = False
    train_cov = LR_CovMat[train_idx, :, :]
    training_class = LR_class[train_idx]

    W_csp = CSP(np.mean(train_cov[training_class==1,:,:],axis=0), np.mean(train_cov[training_class==2,:,:],axis=0))
    F_csp = CSP_Features(LR_trials[train_idx,:,:],W_csp)


    print("F_csp: ", F_csp.shape)
    print("training Class: ", training_class.shape)
    #LDA
    lda = LDA.fit(F_csp,training_class)

    test_features = CSP_Features(LR_trials[test_idx,:,:], W_csp)
    prediction = lda.predict(test_features)

    test_class = LR_class[test_idx]
    ConfusionMatrix[prediction,test_class] = ConfusionMatrix[prediction,test_class]+1

Accuracy = sum(np.diag(ConfusionMatrix))/sum(sum(ConfusionMatrix))
print("Accuracy: ", Accuracy)
