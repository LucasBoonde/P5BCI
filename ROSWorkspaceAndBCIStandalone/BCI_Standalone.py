#!/usr/bin/env python3

"""Denne fil er en kopi af BCI scriptet vi brugte til at plotte de forkellige grafer og tabeller til at vise hvordan vores BCI
fungerer. Der er rettet minimalt i den, og det er mest af alt bare for at sammenligne med hvordan det så ud før, jeg gik igang med at 
fjerne en del overflødige kode stykker fra BCI_script.py"""


#Libraries vi bruger:
import rospy
import time  # Import the time module
import random
import warnings
import matplotlib.pyplot as plt
import sys
import mne
import scipy
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import numpy as np
import moabb
from moabb.datasets import BNCI2014_001
from BCI.msg import BoolStateBCI

#Libraries som er til overs fra implementationen
from std_msgs.msg import String 
import pandas as pd
from scipy.signal import filtfilt
from scipy import stats
import seaborn as sns
from mne.decoding import CSP
from sklearn.pipeline import make_pipeline
from moabb.evaluations import WithinSessionEvaluation
from moabb.paradigms import LeftRightImagery



def BCI_node():
    rospy.init_node('BCI_node', anonymous=True)



    #Changes a setting in Numpy so that it does not shorten any matrices printed in the terminal
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

    #%%--- Extracting data from the given dataset ---:
    sessions = dataset.get_data(subjects=[1])
    subject = 1
    session_name = "0train"
    run_name = "0"


    #Get the raw data from all 22 channels 
    raw = sessions[subject][session_name][run_name]

    #Uncomment to show plot of raw data
    #raw.plot(n_channels=len(raw.ch_names), title='EEG data - Subject {}, Session {}, Run {}'.format(subject, session_name, run_name))
    #plt.show()


    #%%--- Bandpass Filtering---:

    #Ved ikke om dette ændrer data senere i for-loopet, eller om man bare bruger raw data igen?
    raw.filter(l_freq=7, h_freq=30, filter_length='auto', phase='zero')

    #Uncomment to show data after the bandpass filter has been applied
    #raw.plot(n_channels=len(raw.ch_names), title='EEG data - After Bandpass Filter')
    #plt.show()


    #%% --- Extracting Individual Trials ---

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


    for y in stim_channel_values:
        if y != threshold:
            event_sample = events[i]
            stim_value = raw.copy().pick_channels(['stim']).get_data()[0][event_sample]
            for z in range(nbElectrodes):
                currentChannel = raw.ch_names[z]
                trialData = raw.copy().pick_channels([currentChannel])
                if stim_value[0] == 3:
                    channelData = trialData.get_data(start=x, stop=x+(nbSec * fs))
                if i == 0:
                    channelData = trialData.get_data(start=x-250, stop=x+750)
                else:
                    channelData = trialData.get_data(start=x-(nbSec * fs), stop=x)

                Arr2D[z, :] = channelData
            Trials[i, :, :] = Arr2D
            if stim_value[0] == 3:
                Class[i] = 1
            else:
                Class[i] = 2

            Cov[i, :, :] = np.cov(Arr2D)
            i +=1
        x+=1
    print("Class Variables", Class)
    print("Trials Shape: ", Trials.shape)

    #Plotting the Trials of Right hand movement for channel C3
    #plt.plot(Trials[Class==1,7,: ], linewidth=0.5)
    selected_trials = Trials[Class == 1, 0, :]
    num_trials = selected_trials.shape[0]

    # Plot each trial separately
    for i in range(num_trials):
        plt.plot(selected_trials[i, :], linewidth=0.5)

    plt.title("All Right Hand Trials")
    #plt.show()
    print("Selected Trials", selected_trials.shape)
    #print("COVARIANCE MATRIX SHAPE", Cov)
    print("Arr2D Shape", Arr2D.shape)

    #Feature Extraction





    #%% --- COMMON SPATIAL PATTERN (CSP) --- C_right is the 12 right hand movements, C_none are the 36 no hand movement
    C_right = np.mean(Cov[Class == 1, :, :], axis=0)
    C_none = np.mean(Cov[Class == 2, :, :], axis=0)
    C_combined = C_right + C_none

    #We calculate the eigen vector (V) and and eigen value (e) between the covariance matrices right and combined
    e, V = scipy.linalg.eig(C_right, C_combined)



    #We sort the eigen values from high to low
    ind = e.argsort()[::-1]

    #We store the ordered values in the e variable
    e = e[ind]

    #And sort the eigen vectors so they correspond to the new eigen value order
    V = V[ind]
    Vs = V[:, ind]



    """We can now find the eigen vector with the highest eigen value as this is the 0 element in VS. So we got a spatial filter (feature) for 
    W_right for the right hand movement class and a spatial filter (feature) W_None for the no movement class."""
    W_Right = Vs[:, 0]
    W_None = Vs[:, -1]

    #%% -- Plot CSP Features --
    fig, ax = plt.subplots()
    lr_idx = np.any([Class == 1])
    LR_trials = Trials[lr_idx, :, :].reshape((48,22,1000))


    trial = np.squeeze(LR_trials)
    right_feature = np.var(np.dot(W_Right, trial), axis=1)
    none_feature = np.var(np.dot(W_None, trial), axis=1)
    #print("LR_Trials Shape: ", LR_trials.shape)
    colors = Class

    plt.scatter(np.log(right_feature), np.log(none_feature), s=100, c=colors, cmap='bwr_r')

    ax.set(xlabel='log(var(w_1 X))', ylabel='log(var(w_2 X))')
    #plt.show()

    #%% -- LDA Classification --
    def CSP(C1, C2):
        #print("C1", C1.shape)
        #print("C2", C2.shape)
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

    lr_idx = np.any([Class == 1, Class == 2])
    LR_trials_reshaped = Trials[lr_idx, :, :].reshape((48,22,1000))
    #print("LR_trials: ", LR_trials.shape)
    LR_class = Class[lr_idx].reshape((48,))
    #print("LR Class: ", LR_class.shape)
    LR_CovMat = Cov[lr_idx, :, :].reshape((48,22,22))
    #print("LR Cov", LR_CovMat.shape)


    N = LR_trials.shape[0]
    #print("N Size: ", N)

    ConfusionMatrix = np.zeros([2,2])

    for test_idx in range(0,N):
        train_idx = np.ones((48,),dtype=bool)
        train_idx[test_idx] = False
        train_cov = LR_CovMat[train_idx, :, :]
        training_class = LR_class[train_idx]

        W_csp = CSP(np.mean(train_cov[training_class==1,:,:],axis=0), np.mean(train_cov[training_class==2,:,:],axis=0))
        F_csp = CSP_Features(LR_trials_reshaped[train_idx,:,:],W_csp)

        #LDA
        lda = LDA().fit(F_csp,training_class)
        test_features = CSP_Features(LR_trials_reshaped[test_idx,:,:].reshape((1,22,1000)), W_csp)
        #print("Test Features: ",test_features)
        prediction = lda.predict(test_features)


        #y_pred = lda.predict()
        test_class = LR_class[test_idx]
        ConfusionMatrix[int(prediction[0])-1,int(test_class)-1] = ConfusionMatrix[int(prediction[0])-1,int(test_class)-1]+1

    score = lda.score(F_csp,training_class)
    print("SCORE: ",score)

    Accuracy = sum(np.diag(ConfusionMatrix))/sum(sum(ConfusionMatrix))
    print("Accuracy: ", Accuracy)




    # -- Predicting Random Tral --:

    BCIActive = True
    ClassifyCount = 0
    nrOfNoMovement = 0
    nrOfRightMovement=0


    while BCIActive==True:
        test_idx = random.randint(0, N-1)
        train_idx = np.ones((48,), dtype=bool)
        train_idx[test_idx] = False
        train_cov = LR_CovMat[train_idx, :, :]
        training_class = LR_class[train_idx]

        W_csp = CSP(np.mean(train_cov[training_class == 1, :, :], axis=0),
                    np.mean(train_cov[training_class == 2, :, :], axis=0))
        F_csp = CSP_Features(LR_trials_reshaped[train_idx, :, :], W_csp)

        # LDA
        lda = LDA().fit(F_csp, training_class)
        test_features = CSP_Features(LR_trials_reshaped[test_idx, :, :].reshape((1, 22, 1000)), W_csp)

        #Predict the current Class:
        prediction = lda.predict(test_features)
        print("Prediction: ", prediction)
        if prediction == int(1):
            print("Classifier Has Predicted a Movement")
            # Maybe print the actual label for that trial if possible
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


    # Simulate some processing time
    time.sleep(1)  # Change this to the actual duration of your code



    print("Code execution completed. Shutting down node.")




def publishing_node_a():
    rate = rospy.Rate(1)  # 1 Hz    rospy.signal_shutdown("Code execution completed")
    pub = rospy.Publisher('bool_state_topic_BCI', BoolStateBCI, queue_size=10)

    while not rospy.is_shutdown():
        bool_state_msg = BoolStateBCI()
        bool_state_data = True
        bool_state_msg.data = bool_state_data
        pub.publish(bool_state_msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        BCI_node()
        publishing_node_a()
    except rospy.ROSInterruptException:
        pass