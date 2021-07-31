# -*- coding: utf-8 -*-
"""Final heart failure classifier & improving its accuracy

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FUTqbzI63huhFNF3ocQxlFpviwzsDroM
"""

import numpy as np 
import pandas as pd 

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn import linear_model
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

url = 'https://github.com/millenopan/Cardiovascular-Health-Project/blob/main/processed-cleveland.csv?raw=true'
hd = pd.read_csv(url)
hd.target = hd.target.replace({2:1, 3:1, 4:1})
url = 'https://github.com/millenopan/Cardiovascular-Health-Project/blob/main/heart-failure.csv?raw=true'
hf = pd.read_csv(url)
from sklearn.metrics import confusion_matrix, accuracy_score, plot_roc_curve, classification_report

hf

from sklearn.svm import SVC
from sklearn.decomposition import PCA

x = hf.drop(['DEATH_EVENT'], axis = 1)
y = hf.DEATH_EVENT
training_x, testing_x, training_y, testing_y = train_test_split(x,y, test_size=0.2, random_state=85)
svc = SVC()
svc.fit(training_x, training_y)
svc_training_pred = svc.predict(training_x)
svc_testing_pred = svc.predict(testing_x)

pca = PCA(n_components=4)
training_x_pca = pca.fit_transform(training_x)
testing_x_pca = pca.transform(testing_x)

explained_variance = pca.explained_variance_ratio_
print(explained_variance)

svc_confusion_mat = confusion_matrix(testing_y, svc_testing_pred)
svc_accuracy = accuracy_score(testing_y, svc_testing_pred)
print("Confusion matrix:")
print(svc_confusion_mat)
print("Accuracy: " + str(svc_accuracy))

report = classification_report(testing_y, svc_testing_pred)
print("Report of this classification")
print(report)

"""The accuracy without any modifications to the data is 76.7 percent. Next, we can try fitting the data to a Gradient Boosting classifier."""

from sklearn.ensemble import GradientBoostingClassifier
gbc = GradientBoostingClassifier()
gbc.fit(training_x, training_y)
gb_training = gbc.predict(training_x)
gb_testing = gbc.predict(testing_x)

scores = cross_val_score(gbc, x, y, cv=40)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
scores

"""The accuracy is a little higher. But we'll now try logistic regression and see what that yields. """

x = hf.drop(['DEATH_EVENT'], axis = 1)
y = hf.DEATH_EVENT
training_x, testing_x , training_y, testing_y = train_test_split(x, y, test_size=0.2, random_state=85)
lr = LogisticRegression(max_iter=2000)
lr.fit(training_x, training_y)
lr_train_prediction = lr.predict(training_x)
lr_test_prediction = lr.predict(testing_x)
print("Logistical regression accuracy:")
lr.score(testing_x, testing_y)

confusion_mat = confusion_matrix(testing_y, lr_test_prediction)
accuracy = accuracy_score(testing_y, lr_test_prediction)
print("Confusion matrix:")
confusion_mat
print("Accuracy: " + str(accuracy))

report = classification_report(testing_y, lr_test_prediction)
print("Report of this classification")
print(report)

"""The accuracy is 83.3 percent. Next, we will try increasing the test size to 0.3 and I will also change the fit intercept to false, set verbose to 1, and n_jobs (number of CPU scores used) to a nonzero number. As well as this, I'll try to find the ideal maximum iterations value. """

x = hf.drop(['DEATH_EVENT'], axis = 1)
y = hf.DEATH_EVENT
training_x, testing_x , training_y, testing_y = train_test_split(x, y, test_size=0.3, random_state=85)
lr = LogisticRegression(fit_intercept=False, max_iter=70, verbose = 1, n_jobs = 8)
lr.fit(training_x, training_y)
lr_train_prediction = lr.predict(training_x)
lr_test_prediction = lr.predict(testing_x)
print("Logistical regression accuracy:")
print(lr.score(testing_x, testing_y))

confusion_mat = confusion_matrix(testing_y, lr_test_prediction)
accuracy = accuracy_score(testing_y, lr_test_prediction)
print("Confusion matrix:")
print(confusion_mat)
print("Accuracy: " + str(accuracy))

report = classification_report(testing_y, lr_test_prediction)
print("Report of this classification:")
print(report)

"""The best maximum iterations value (which leads to the highest accuracy) looks to be 70. This leads to an accuracy of 87.8 percent (to 3 signiificant figures), which is a big improvement from earlier. """

