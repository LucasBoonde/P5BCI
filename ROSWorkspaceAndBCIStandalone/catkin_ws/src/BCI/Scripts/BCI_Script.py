#!/usr/bin/env python3

import rospy
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

    #%%--- Extracting data from a given dataset ---:
    sessions = dataset.get_data(subjects=[1])
    subject = 1
    session_name = "0train"
    run_name = "0"


    #Get the raw data from all 22 channels 
    raw = sessions[subject][session_name][run_name]



    #%%--- Bandpass Filtering---:ø
    raw.filter(l_freq=7, h_freq=30, filter_length='auto', phase='zero')


    #%% --- Separating the data into individual trials ---
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

    #Now we want to extract this MNE array into a standard 1D array. This is stored in the variable stim_channel_values
    stim_channel_values = stim_channel_data.get_data()[0]

    Arr2D = np.zeros([len(raw.ch_names) - 4, nbSec * fs])



    """Placeholder variables to keep track of what indexes we are at in the 3D array."""
    i = 0  #Keeps track of the 48 stims. The first stim comes 250 samples in, so since we cant take 1000 samples before, we have to take -250 and +750.
    x = 0  #Keeps track of the sample number from 0 to 96735
    noStim = 0 #Defines stim values = 0 as noStim samples


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

            Cov[i, :, :] = np.cov(Arr2D) 
            i +=1
        x+=1



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
        prediction = lda.predict(test_features)


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
        print("Number of no movements detected: ", nrOfNoMovement)
        
    print("Right Hand Movement Classified", nrOfRightMovement)



    # Simulate some processing time
    time.sleep(1)  # Change this to the actual duration of your code



    print("BCI prediction completed. Initiating publisher node.")




def publishing_node_a():
    rate = rospy.Rate(1)  # 1 Hz    rospy.signal_shutdown("Code execution completed")
    pub = rospy.Publisher('bool_state_topic_BCI', BoolStateBCI, queue_size=10)
    print("Publisher node initiated and sending data to topic")
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