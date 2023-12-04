import warnings
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import sys
import mne
import moabb
from moabb.datasets import BNCI2014_001
from moabb.paradigms import LeftRightImagery
from mne import Epochs, events_from_annotations, pick_types
from mne.channels import make_standard_montage
from mne.decoding import CSP
from mne.io import concatenate_raws, read_raw_edf

import matplotlib.pyplot as plt
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import ShuffleSplit, cross_val_score
from sklearn.pipeline import Pipeline

np.set_printoptions(threshold=sys.maxsize)

dataset = BNCI2014_001()
dataset.subject_list[1]

sessions = dataset.get_data(subjects=[1])
subject = 1
session_name = "0train"
run_name = "0"

tmin, tmax = 0.0, 4.0


# Import Data
raw = sessions[subject][session_name][run_name]
raw.plot(n_channels=len(raw.ch_names), title='Raw EEG data - Subject {}, Session {}, Run {}'.format(subject, session_name, run_name))
plt.show()
#print("raw info", raw.info)

print("Channels", raw.ch_names)


#Bandpass filtering
raw.filter(l_freq=7, h_freq=30, filter_length='2s', phase='zero')
#raw.plot(n_channels=len(raw.ch_names), title='Filtered EEG data - Subject {}, Session {}, Run {}'.format(subject, session_name, run_name))

plt.show()


#Extracting Epochs - Only right_hand class and no class
events = mne.find_events(raw, stim_channel="stim")



event_dict = {"tongue":4, "feet":3, "right_hand":2, "left_hand":1}
print("Event values", events==event_dict.values())

picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False, exclude="bads")

#Showing the picked epochs
#fig = mne.viz.plot_events(events, event_id=event_dict, sfreq=raw.info["sfreq"], first_samp=raw.first_samp) #Shows the stim events and id's


epochs = Epochs(
    raw,
    events,
    event_id=event_dict,
    tmin=tmin,
    tmax=tmax,
    proj=True,
    picks=picks,
    baseline=None,
    preload=True,
)

labels = epochs.events[:,-1]
print("Labels: ", labels)

epochs_data = epochs.get_data()
#print("epochs_data Shape: ", epochs_data[0,7,:])
print("epochs_data Shape: ", epochs_data.shape)


#Show the trials for one channel (Just as as test to see if there are any similar data)
#fig, ax = plt.subplots(layout="constrained")
rightHand = event_dict.values()

plt.plot(epochs_data[events[:,2]==2,7,:], linewidth = 0.5)
#plt.scatter(epochs_data[0,11,:], epochs_data[0,11,:])
plt.xlabel('Samples')
plt.ylabel('Channel C3 for 48 trials')
plt.show()

plt.style.use('seaborn')
plt.scatter(epochs_data[:,7,:], epochs_data[:,11,:])
plt.xlabel('Channel C3')
plt.ylabel('Channel C4')
plt.show()



#Feature Exctraction - Try only a single channel and one try



#CSP - show covariance between the 3 features on C3 and C4?



#LDA generer parametrene y=theta*X+b: hvor X er vores matrix af data, thetaer det indre produkt for det givne trial og b er forskydningen fra origo til theta.



#Predict function: y=sign(var((theta) X)+b)



#Tuning af classifier