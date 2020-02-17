from classifier import Classifier

import numpy as np
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsClassifier

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
    def generate_group_data(cluster_size, clusters_number):
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
        
    def generate_random_data(cluster_size, clusters_number):
        x = np.zeros((cluster_size * clusters_number,2))
        y = np.zeros(cluster_size*clusters_number)
        for i in range(clusters_number * cluster_size):
            x[i] = np.random.rand(2)
            y[i] = np.random.randint(0,clusters_number)
        return x,y
        
    data, labels = generate_group_data(100,2)
    #data, labels = generate_random_data(100,5)
    
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2,4)
    
    data_distr = fig.add_subplot(gs[0,0])
    data_distr.title.set_text("Data distribution")
    data_distr.axis((0,1,0,1))
    data_distr.scatter(*data.T, c = labels)
    
    knn = KNNClassifier()
    knn.fit(data, labels)
    
    xx, yy = np.meshgrid(np.arange(-0.1, 1.1, 0.1), np.arange(-0.1, 1.1, 0.1))
    
    N = 1000
    
    xs = np.random.rand(N,2)
    for i in range(3):
        cs = np.zeros(N)
        
        k = (i+1)*2
        
        for j in range(N):
            cs[j] = knn.predict(xs[j], k)
            
        res = fig.add_subplot(gs[0,i+1])
        res.title.set_text("Predictions with k = " + str(k))
        Z = []
        for z in np.c_[xx.ravel(), yy.ravel()]:
            Z.append(knn.predict(z, k))
        Z = np.array(Z).reshape(xx.shape)
        res.contourf(xx, yy, Z, cmap=plt.cm.RdBu, alpha=.8)
        res.scatter(*xs.T, c = cs)
        res.axis((0,1,0,1))
        
        sk_knn =  KNeighborsClassifier(n_neighbors=k)
        sk_knn.fit(data, labels)
        
        sk_res = fig.add_subplot(gs[1,i+1])
        sk_res.title.set_text("sklearn predictions with k = " + str(k))
        cs = sk_knn.predict(xs)
        Z = sk_knn.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        sk_res.contourf(xx, yy, Z, cmap=plt.cm.RdBu, alpha=.8)
        sk_res.scatter(*xs.T, c = cs)
        sk_res.axis((0,1,0,1))
        
    plt.show()

if __name__ == "__main__":
    test()