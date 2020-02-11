import numpy as np

# sceleton for different classiffiers aka virtual class :)
class Classifier:
    def __init__(self, learning_rate = 0.01, iterations = 1000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        
    # creates all needed stuff for further fitting process
    def prefit(self, input, output):
        dim_in = input.shape[1]
        dim_out = output.shape[1]
        
        self.weights = np.random.rand(dim_in, dim_out)
        self.bias = np.random.rand(dim_out)
        self.history = np.zeros(self.iterations)
        
    def fit(self, input, output):
        pass
    
    def predict(self,x):
        pass
        
    def error(self, input, output):
        pass