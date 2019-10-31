import numpy as np

import random

def sigmoid(x):
    return 1/(1+np.exp(-x))

class Perceptron:
    def __init__(self,layer_sizes):
        self.num_layers = len(layer_sizes)
        self.layer_sizes = layer_sizes
        self.biases = [np.random.randn(x,1) for x in self.layer_sizes[1:]]
        self.weight = [np.random.randn(y,x) for x,y in zip(self.layer_sizes,self.layer_sizes[1:])]
        
    def predict(self,imput):
        out = input
        for w,b in zip(self.weight,self.biases):
            out = sigmoid(np.dot(w,out) + b)
        return out
        
    """ SGD - stochastic gradient descent """
    def trainSGD(self,training_data,epochs,mini_batch_size,learning_rate):
        for i in range(epochs):
            random.shuffle(training_data)
            k = random.randint(0,len(training_data))
            mini_batch = training_data[k:k+mini_batch_size]
            
        
if __name__=="__main__":
    k = random.randint(0,len([1,2,3,4,5,6]))