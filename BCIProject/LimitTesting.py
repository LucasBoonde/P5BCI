import numpy as np
import scipy.io
import matplotlib.pyplot as plt


class LDA:
    def __init__(self, n_components):
        self.n_components = n_components
        self.linear_discriminants = None

    def fit(self,X, y):
        n_features = X.shape[1]
        class_lables = np.unique(y)

        #S_W, S_B
        mean_overall = np.mean(X,axis=0) #1000, 2
        S_W = np.zeros((n_features, n_features)) #2,2
        S_B = np.zeros(n_features,n_features) #2,2

        for c in class_lables:
            X_c = X[y==c]
            mean_c = np.mean(X_c, axis=0)
            # 2,2
            S_W +=(X_c - mean_c).T.dot(X_c - mean_c)

            n_c = X_c.shape[0]
            # (2,1)*(2,1)T = 2,2
            mean_diff = (mean_c-mean_overall).reshape(n_features, 1) #for at få en 2,1 matrix
            S_B += n_c * (mean_diff).dot(mean_diff).T

        A = np.linalg.inv(S_W).dot(S_B)

        eigenvalues, eigenvectors = np.linalg.eig(A)
        eigenvectors = eigenvectors.T
        idxs = np.argsort(abs(eigenvalues))[::-1]
        eigenvalues = eigenvalues[idxs]
        eigenvectors = eigenvectors[idxs]
        self.linear_discriminants = eigenvectors[0:self.n_components]


    def transform(self, X):
        #Project Data onto new component
        return np.dot(X,self.linear_discriminants.T)


class PCA:
    def __init__(self, n_components):
        self.n_components = n_components
        self.components = None
        self.mean = None

    def fit(self, X):
        # mean
        self.mean = np.mean(X, axis=0)
        X=X-self.mean

        # Covariance
        cov = np.cov(X.T)#Måske skal den ikke transponeres.

        #eigenvectors, eigenvalues
        eigenvalues, eigenvectors = np.linalg.eig(cov)
        # Eigenvectors are returned as column vectors and therefore we need to transpose
        eigenvectors=eigenvectors.T

        # sort eigenvectors
        #[::-1] Slicer alt data i decreasing order
        idxs = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idxs]
        eigenvectors=eigenvectors[idxs]

        #store first n eigenvectors
        self.components = eigenvectors[0,self.n_components]
    def transform(self, X):
        # Project data
        X = X-self.mean
        return np.dot(X,self.components.T)






