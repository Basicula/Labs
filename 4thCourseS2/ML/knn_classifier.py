from classifier import Classifier

import numpy as np
import matplotlib.pyplot as plt

def euler_dist(x, y):
    return np.linalg.norm(x-y)

class KNNClassifier(Classifier):
    def __init__(self):
        super().__init__()
        
    def fit(self, input, output):
        self.input = input
        self.output = output
    
    def predict(self, x, k, dist_func=euler_dist):
        indices = np.arange(len(self.input))
        nearest_k_neighbors = sorted(indices, key = lambda i: dist_func(self.input[i], x))[:k]
        outputs_for_neighbors = list(self.output[nearest_k_neighbors])
        dominant_neighbor = max(set(outputs_for_neighbors), key = outputs_for_neighbors.count)
        return dominant_neighbor
        
    def error(self, input, output):
        pass
        
if __name__ == "__main__":
    knn = KNNClassifier()
    def generate_data(cluster_size, clusters_number, dims):
        x = np.zeros((cluster_size * clusters_number,dims))
        y = np.zeros(cluster_size*clusters_number)
        index = 0
        for j in range(clusters_number):
            center = np.random.rand(dims)
            for i in range(cluster_size):
                delta = (np.random.rand(dims)-0.5)*0.7
                x[index] = delta*np.linalg.norm(delta)+center
                y[index] = j
                index+=1
        return x,y
        
    data,labels = generate_data(100,6,2)
    plt.axis((0,1,0,1))
    plt.scatter(*data.T, c = labels)
    plt.show()
    
    knn.fit(data, labels)
    N = 2000
    
    xs = np.random.rand(N,2)
    cs = np.zeros((N))
    
    for i in range(N):
        cs[i] = knn.predict(xs[i],4)
        
    plt.scatter(*xs.T, c = cs)
    plt.show()