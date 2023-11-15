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

np.set_printoptions(threshold=sys.maxsize)

moabb.set_log_level("info")
warnings.filterwarnings("ignore")

#Get the desired Dataset and choose amount of subjects.
dataset = BNCI2014_001()
dataset.subject_list[1]

#Get data from given sesion
#Number of Subjects = 10
#Number of Channels = 22 + 3 EOG
#Number og Classes = 4(rh, lh, feet, tongue)
#Trials/Class = 144
#Trials Length = 4sec
#Sampling Rate = 250Hz
#Sessions = 2
sessions = dataset.get_data(subjects=[1])

subject = 1
session_name = "0train"
run_name = "0"

#

raw = sessions[subject][session_name][run_name]
#raw.plot(n_channels=len(raw.ch_names), title='EEG data - Subject {}, Session {}, Run {}'.format(subject, session_name, run_name))
#plt.show()
###



#Bandpass Filtering:

#For only filtering specific channels:
#channel_to_filter = 'Fz'

#raw.filter(l_freq=0.5, h_freq=30, filter_length='auto', phase='zero')
#raw.plot(n_channels=len(raw.ch_names), title='EEG data - After Bandpass Filter')

#plt.show()


#Extracting Individual Trials
"""Hvert run har flere runs, og vi kan inddele dem i trials, 
så vi senere kan predicte om det er en action eller ej"""

fs = 250
nbSec = 4
TrialDuration = fs*nbSec
nbTrials = 48
#Trials pr class pr run = 12
#Total amount of runs = 12
nbSecs = 385
nbElectrodes = 22
nbSubjects = 10

#len(raw.ch_names)-4 fordi vi kun bruger EEG Channels, men kan ændres senere.
Trials = np.zeros((nbTrials, len(raw.ch_names)-4, nbSec*fs))
Class = np.zeros((nbTrials, 1))


Cov = np.zeros((nbTrials, nbSubjects, nbElectrodes))

i = 0
#for trial in range(nbTrials):



# Check if 'stim' channel exists in the data
if 'stim' in raw.ch_names:
    stim_channel_data = raw.copy().pick_channels(['stim'])

    # Extract the values from the 'stim' channel
    stim_channel_values = stim_channel_data.get_data()[0]
    threshold = 0

    x = 0
    z = 0
    Arr2D = np.zeros([len(raw.ch_names) - 4, nbSec * fs])

    for y in stim_channel_values:

        if y != threshold:
            #print(x/fs)
            for z in range(nbElectrodes):
                currentChannel = raw.ch_names[z]
                trialData = raw.copy().pick_channels([currentChannel])
                channelData = trialData.get_data(start=x, stop=x+(nbSec * fs))
                #print("Data From: ", currentChannel)
                #print("Electrode: ", z+1)
                #print("From X value", x)
                #print("Current Stim", i + 1)
                #print("--------------------- NEXT ---------------------")
                #print(channelData.shape)
                #print("Arr2D", Arr2D.shape)
                # Use ':' instead of '(z, :)' for indexing
                Arr2D[z, :] = channelData
                #print(Arr2D)
            Trials[i, :, :] = Arr2D
            i +=1
        x+=1

    #print(Trials)

    # Plotting the first trial
    trial_to_plot = 0

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extracting x, y, and z coordinates from Trials
    x = range(nbSec * fs)
    y = range(len(raw.ch_names) - 4)
    X, Y = np.meshgrid(x, y)
    Z = Trials[trial_to_plot, :, :]

    # Plotting the surface
    ax.plot_surface(X, Y, Z, cmap='viridis')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Electrodes')
    ax.set_zlabel('Amplitude')

    plt.title(f'Trial {trial_to_plot + 1}')
    plt.show()

    #Trials = Trials[1:i,:,:]


else:
    print("The 'stim' channel is not present in the data.")












