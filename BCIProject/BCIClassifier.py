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

#%% --- Setup for MOABB ---
moabb.set_log_level("info")
warnings.filterwarnings("ignore")

dataset = BNCI2014_001()
dataset.get_data()

#%%--- Extracting data from a given dataset ---:

sessions = dataset.get_data(subjects=[1])

#subject = 1
#session_name = "0train"
#run_name = "0"

#Can be changed to include multiple sessions or patients.
subject = 1
session_name = "0train"
run_name = "0"

tmin, tmax = 0.0, 4.0

raw = sessions[subject][session_name][run_name]
raw.filter(l_freq=0.5, h_freq=30, filter_length='auto', phase='zero')

events = mne.find_events(raw, stim_channel="stim")

print("raw info", raw.info)


#events, _ = events_from_annotations(raw, event_id=dict(T1=2, T2=3))
#print("events", events[:20]) # shows the first 20 stims

event_dict = {"tongue":4, "feet":3, "right_hand":2, "left_hand":1}

fig = mne.viz.plot_events(events, event_id=event_dict, sfreq=raw.info["sfreq"], first_samp=raw.first_samp) #Shows the stim events and id's

picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False, exclude="bads")

epochs = Epochs(
    raw,
    events,
    event_id=2,
    tmin=tmin,
    tmax=tmax,
    proj=True,
    picks=picks,
    baseline=None,
    preload=True,
)

epochs_train = epochs.copy().crop(tmin=1.0, tmax=2.0)
labels = epochs.events[:,-1]-2 #ved ikke hvorfor man vil have -2?
print("Labels: ", labels)
#print("Epochs Data: ", epochs.get_data())

# --- CSP ---
scores = []
epochs_data = epochs.get_data()
epochs_data_train = epochs_train.get_data()
cv = ShuffleSplit(10, test_size=0.2, random_state=42) #Parametre for Cross-validation
cv_split = cv.split(epochs_data_train)

#The Classifier
lda = LinearDiscriminantAnalysis()
csp = CSP(n_components=2, reg=None, log=True, norm_trace=False)

#Cross Validation using Scikit-learn Pipeline:
clf = Pipeline([("CSP", csp), ("LDA", lda)])
scores = cross_val_score(clf,epochs_data_train,labels,cv=cv,n_jobs=None)

print("scores", scores)

class_balance = np.mean(labels == labels[0])
class_balance = max(class_balance, 1.0-class_balance)
print("Classification Accuracy: %f/ Chance Level: %f" %(np.mean(scores),class_balance))

#Plots CSP patterns estimated on the full data visualization
csp.fit_transform(epochs_data, labels)

csp.plot_patterns(epochs.info, ch_type="eeg", units="patterns (Righ Hand)", size=1.5)
plt.show()

# Performance over time
sfreq  = raw.info["sfreq"] #outputter bare sample frekvens
w_lenght = int(sfreq*0.5) #Running Classifier: window length
w_step = int(sfreq*0.1) #Running classifier: window step size
w_start = np.arange(0,epochs_data.shape[2]-w_lenght,w_step)

scores_window = []

#For-loop that trains the classifier over time
sfreq = raw.info["sfreq"]
w_length = int(sfreq * 0.5)  # running classifier: window length
w_step = int(sfreq * 0.1)  # running classifier: window step size
w_start = np.arange(0, epochs_data.shape[2] - w_length, w_step)

scores_windows = []

for train_idx, test_idx in cv_split:
    y_train, y_test = labels[train_idx], labels[test_idx]

    X_train = csp.fit_transform(epochs_data_train[train_idx], y_train)
    X_test = csp.transform(epochs_data_train[test_idx])

    # fit classifier
    lda.fit(X_train, y_train)

    # running classifier: test classifier on sliding window
    score_this_window = []
    for n in w_start:
        X_test = csp.transform(epochs_data[test_idx][:, :, n : (n + w_length)])
        score_this_window.append(lda.score(X_test, y_test))
    scores_windows.append(score_this_window)

# Plot scores over time
w_times = (w_start + w_length / 2.0) / sfreq + epochs.tmin

plt.figure()
plt.plot(w_times, np.mean(scores_windows, 0), label="Score")
plt.axvline(0, linestyle="--", color="k", label="Onset")
plt.axhline(0.5, linestyle="-", color="k", label="Chance")
plt.xlabel("time (s)")
plt.ylabel("classification accuracy")
plt.title("Classification score over time")
plt.legend(loc="lower right")
plt.show()


