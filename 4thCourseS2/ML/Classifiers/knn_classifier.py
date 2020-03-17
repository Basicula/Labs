from classifier import Classifier
from data_generator import DataGenerator, split_data
from utils import add_plot_model_predictions, add_plot_data_2d, add_plot_with_roc_curve

import numpy as np
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsClassifier

def euler_dist(x, y):
    return np.linalg.norm(x-y)

class KNNClassifier(Classifier):
    def __init__(self, k = 10):
        super().__init__()
        self.k = k
        
    def fit(self, input, output):
        self.input = input
        self.output = output
        self.indices = np.arange(len(self.input))
    
    def predict(self, xs, dist_func=euler_dist):
        res = np.zeros(len(xs))
        for i, x in enumerate(xs):
          nearest_k_neighbors = sorted(self.indices, key = lambda i: dist_func(self.input[i], x))[:self.k]
          outputs_for_neighbors = list(self.output[nearest_k_neighbors])
          dominant_neighbor = max(set(outputs_for_neighbors), key = outputs_for_neighbors.count)
          res[i] = dominant_neighbor
        return res
        
    def predict_proba(self, xs, dist_func=euler_dist):
        res = np.zeros((len(xs), len(set(self.output))))
        for i, x in enumerate(xs):
          nearest_k_neighbors = sorted(self.indices, key = lambda i: dist_func(self.input[i], x))[:self.k]
          outputs_for_neighbors = self.output[nearest_k_neighbors]
          for c in set(list(outputs_for_neighbors)):
            res[i][c] = sum(outputs_for_neighbors==c) / len(outputs_for_neighbors)
        return res
        
    def error(self, input, output):
        pass

def test_with_roc(classes=2):
    data, labels = DataGenerator.random_2d(100,classes)
    labels = labels.ravel()
    trainX, trainY, testX, testY = split_data(data, labels)
    
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2,2+classes)
    
    N = 1000
    axis = (0,1,0,1)
    
    data_distr = add_plot_data_2d(fig, gs[0,0], data, labels, "Data distribution", axis)

    knn = KNNClassifier(10)
    knn.fit(data, labels)
    
    res = add_plot_model_predictions(fig, gs[0,1], testX, knn, "Predictions", axis, True)
    
    sk_knn =  KNeighborsClassifier(n_neighbors=10)
    sk_knn.fit(data, labels)
    
    sk_res = res = add_plot_model_predictions(fig, gs[1,1], testX, sk_knn, "sklearn predictions", axis, True)
        
    for c in range(classes):
        add_plot_with_roc_curve(fig, gs[0,2+c], testY==c, knn.predict_proba(testX)[:,c], "ROC for class " + str(c))
        add_plot_with_roc_curve(fig, gs[1,2+c], testY==c, sk_knn.predict_proba(testX)[:,c], "sklearn ROC for class " + str(c))
        
    plt.show()

def test(k_cnt, classes=2):
    data, labels = DataGenerator.blobs_2d(100,classes)
    labels = labels.ravel()
    
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2,1+k_cnt)
    
    N = 1000
    axis = (0,1,0,1)
    
    data_distr = add_plot_data_2d(fig, gs[0,0], data, labels, "Data distribution", axis)
    
    xs = np.random.rand(N,2)
    for i in range(k_cnt):
        k = (i+1)*2
        
        knn = KNNClassifier(k)
        knn.fit(data, labels)
        
        res = add_plot_model_predictions(fig, gs[0,i+1], xs, knn, "Predictions with k = ", axis, True)
        
        sk_knn =  KNeighborsClassifier(n_neighbors=k)
        sk_knn.fit(data, labels)
        
        sk_res = res = add_plot_model_predictions(fig, gs[1,i+1], xs, sk_knn, "sklearn predictions with k = " + str(k), axis, True)
        
    plt.show()

if __name__ == "__main__":
    test(3,5)
    test_with_roc(3)