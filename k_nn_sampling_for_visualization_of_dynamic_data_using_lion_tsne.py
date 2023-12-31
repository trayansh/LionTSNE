# -*- coding: utf-8 -*-
"""k-NN Sampling for Visualization of Dynamic data using LION-tSNE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dWZJ-b3USAyuQ9XePaFGt4gyLH4PGdwi
"""

!pip install plotly_express
!pip install pyDOE2
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn.datasets import load_iris
import plotly_express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from pyDOE2 import lhs
from sklearn.metrics import accuracy_score
#X is the Data of Dataset
X = iris.data
# Y is the lables
Y = iris.target

def KNN_sampling(X,y,k):

  train_sample = []
  Y =[]

  while(len(X)>k):
    neigh = KNeighborsClassifier(n_neighbors=k,algorithm='ball_tree').fit(X,y)
    indices = neigh.kneighbors(X, return_distance = False)
    NN_scores = []
    MNN_scores = []
    # Calculation of MNN and NN Scores
    neighbors = {i:set() for i in range(len(X))}
    M_neighbors = {i:set() for i in range(len(X))}
    for i in range(len(X)):
      xi = X[i]
      mnn = []
      for j in indices[i]:
        xj = X[j]
        if i != j:
          neighbors[j].add(i)

          mutual_neighbor = set(indices[i][1:]).intersection(indices[j][1:])

          if xi in X[list(mutual_neighbor)] and xj in X[list(mutual_neighbor)]:
            mnn.extend(mutual_neighbor)

      MNN_scores.append(len(set(mnn)))
      for t in mnn:
        M_neighbors[i].add(t)

    for i in range(len(X)):
      NN_scores.append(len(neighbors[i]))

    # Calculation of Index

    index = [i for i,x in enumerate(NN_scores) if(x == np.max(NN_scores))]

    if(len(index)>1):
      temp_index = [MNN_scores[i] for i in index]
      train_index = index[temp_index.index(np.max(temp_index))]
    else:
      train_index = index[0]

    train_sample.append(X[train_index])
    Y.append(y[train_index])
    X = np.delete(X,train_index,axis=0)
    y = np.delete(y,train_index,axis=0)
    for n_index in M_neighbors[train_index]:
      if n_index < X.shape[0]:
        X = np.delete(X,n_index,axis=0)
        y = np.delete(y,n_index,axis=0)

        # (t,m,s)Net For Reamining X Sampling
  if(len(X) !=0):
    num_samples = X.shape[0]
    num_dimensions = X.shape[1]
    lhs_samples = lhs(num_dimensions, num_samples)
    Y.extend(y)
    for sample in lhs_samples:
      train_sample.append(sample)

  return train_sample, Y

#KNN Sampling
train_sample,train_sample_result = KNN_sampling(X,Y,10)

#TSNE for HD to LD
tsne_results=[]
train_sample_tsne = TSNE(n_components = 3, perplexity = 10, random_state=32).fit_transform(np.array(train_sample))
tsne_results.append(train_sample_tsne)

#KNN accuracy
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(np.array(tsne_results[0]), train_sample_result)
y_pred = knn.predict(tsne_results[0])
accuracy_score(train_sample_result,y_pred)


# KNN Sampling
train_sample, train_sample_result = KNN_sampling(X, Y, 10)

# TSNE for HD to LD
tsne_results = []
test_tsne_results = []

train_sample_tsne = TSNE(n_components=3, perplexity=10, random_state=32).fit_transform(np.array(train_sample))
test_sample_tsne = TSNE(n_components=3, perplexity=10, random_state=32).fit_transform(np.array(iris.data))

tsne_results.append(train_sample_tsne)
test_tsne_results.append(test_sample_tsne)


# KNN accuracy
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(np.array(tsne_results[0]), train_sample_result)
y_pred = knn.predict(test_tsne_results[0])
accuracy = accuracy_score(Y, y_pred)
print("Accuracy:", accuracy)

df = pd.DataFrame(iris.data,columns=iris.feature_names)
m=px.scatter_3d(df, x="sepal length (cm)", y="petal width (cm)", z="sepal width (cm)", size="petal length (cm)",
              color=iris.target, color_discrete_map = {"Joly": "blue", "Bergeron": "violet", "Coderre":"pink"})
m.show()

df = pd.DataFrame(np.array(tsne_results[0]),columns=["1","2","3"])
m=px.scatter_3d(df, x="1", y="2", z="3",
              color=train_sample_result, color_discrete_map = {"Joly": "blue", "Bergeron": "violet", "Coderre":"pink"})
m.show()

