#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = 'Feng Wang (Felix)'
__email__ = 'wangfelix87@gmail.com'
__date__ = '06-05-2015'

class BaseClassifier:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def fit(self, X, y):
        """
        Fit the model according to the given training data

        Parameters
        ----------
        X: {array-like}, shape (n_samples, n_features)
            Training vector, where n_samples is the number of samples and
            n_features is the number of features

        y: array-like, shape (n_samples,)
            Target vector relative to X.

        Returns
        -------
        self : object
            return self.
        """
        pass

    def predict_proba(self, X):
        """
        Probability estimates.

        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]

        Returns
        -------
        T : array-like, shape = [n_samples, n_classes]
            Returns the probability of the sample for each class in the model
        """
        pass

    def predict(self, X):
        """
        Class estimates.

        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]

        Returns
        -------
        yhat: array-like, shape = (n_samples, )
            Returns the predicted class of the sample
        """
        pass


    def evaluate(self, X, y, metric = 'AUC'):
        """
        Evaluate the classifier

        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]

        Returns
        -------
        score: the evaluation score of metric given
        """
        pass

    def print_coefficients(self):
        pass
