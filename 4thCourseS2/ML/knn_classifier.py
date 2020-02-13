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
        self.indices = np.arange(len(self.input))
    
    def predict(self, x, k, dist_func=euler_dist):
        nearest_k_neighbors = sorted(self.indices, key = lambda i: dist_func(self.input[i], x))[:k]
        outputs_for_neighbors = list(self.output[nearest_k_neighbors])
        dominant_neighbor = max(set(outputs_for_neighbors), key = outputs_for_neighbors.count)
        return dominant_neighbor
        
    def error(self, input, output):
        pass

def test():
    def generate_data(cluster_size, clusters_number):
        x = np.zeros((cluster_size * clusters_number,2))
        y = np.zeros(cluster_size*clusters_number)
        index = 0
        for j in range(clusters_number):
            center = np.random.rand(2)
            for i in range(cluster_size):
                delta = (np.random.rand(2)-0.5)*0.5
                x[index] = delta*np.linalg.norm(delta)+center
                y[index] = j
                index+=1
        return x,y
        
    data, labels = generate_data(100,5)
    
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2,3)
    
    data_distr = fig.add_subplot(gs[0,0])
    data_distr.title.set_text("Data distribution")
    data_distr.axis((0,1,0,1))
    data_distr.scatter(*data.T, c = labels)
    
    knn = KNNClassifier()
    knn.fit(data, labels)
    
    N = 2000
    
    xs = np.random.rand(N,2)
    for i in range(5):
        cs = np.zeros(N)
        
        k = (i+1)*2
        
        for j in range(N):
            cs[j] = knn.predict(xs[j], k)
            
        res = fig.add_subplot(gs[(i+1)//3,(i+1)%3])
        res.title.set_text("Predictions with k = " + str(k))
        res.scatter(*xs.T, c = cs)
    
    plt.show()

if __name__ == "__main__":
    test()