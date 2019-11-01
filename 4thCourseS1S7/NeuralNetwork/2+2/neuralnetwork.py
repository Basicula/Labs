import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist
import random

def sigmoid(x):
    return 1/(1+np.exp(-x))
    
def sigmoid_prime(x):
    return sigmoid(x)*(1-sigmoid(x))

class Perceptron:
    def __init__(self,layer_sizes):
        self.num_layers = len(layer_sizes)
        self.layer_sizes = layer_sizes
        self.biases = [np.random.randn(1,x) for x in self.layer_sizes[1:]]
        self.weights = [np.random.randn(x,y) for x,y in zip(self.layer_sizes,self.layer_sizes[1:])]
        
    def predict(self,input):
        out = input
        for w,b in zip(self.weights,self.biases):
            out = sigmoid(np.dot(out,w) + b)
        return out
        
    """ SGD - stochastic gradient descent """
    def trainSGD(self,training_data,epochs,mini_batch_size,learning_rate):
        for i in range(epochs):
            random.shuffle(training_data)
            k = random.randint(0,len(training_data)-mini_batch_size)
            mini_batch = training_data[k:k+mini_batch_size]
            db_sum = [np.zeros(b.shape) for b in self.biases]
            dw_sum = [np.zeros(w.shape) for w in self.weights]
            for x,y in mini_batch:
                db,dw = self.backpropagation(x,y)
                db_sum += db
                dw_sum += dw
            self.weights = [w+dw for w,dw in zip(self.weights,dw_sum)]
            self.biases = [b+db for b,db in zip(self.biases,db_sum)]
                
    def backpropagation(self,x,y):
        db = [np.zeros(b.shape) for b in self.biases]
        dw = [np.zeros(w.shape) for w in self.weights]
        
        activations = [x]
        results = []
        for b,w in zip(self.biases,self.weights):
            result = np.dot(activations[-1],w) + b
            results.append(result)
            activations.append(sigmoid(result))
            
        diff = y-activations[-1]
        
        dloss = 2*diff*sigmoid_prime(results[-1])
        db[-1] = dloss
        dw[-1] = activations[-2].T.dot(dloss)
        for i in range(2,self.num_layers):
            dloss = dloss.dot(self.weights[-i+1].T)*sigmoid_prime(results[-i])
            db[-i] = dloss
            dw[-i] = activations[-i-1].T.dot(dloss)
        return db,dw
        
if __name__=="__main__":
    x = [np.reshape(i,(1,2)) for i in np.array([[0,0],[0,1],[1,0],[1,1]])]
    y = np.array([0,1,1,0]).T
    p = Perceptron([2,4,1])
    p.trainSGD(list(zip(x,y)),60000,1,1)
    print(p.weights)
    print(p.biases)
    print(p.predict(np.reshape(np.array([0,0]),(1,2))))
    
    #p = Perceptron([784,30,10])
    #(x_train, y_train), (x_test, y_test) = mnist.load_data()
    #x_train = [np.reshape(x,(1,784))/255 for x in x_train]
    #y_train_vectors = []
    #for y in y_train:
    #    vec = np.zeros((10,1))
    #    vec[y] = 1.0
    #    y_train_vectors.append(vec)
    #p.trainSGD(list(zip(x_train,y_train_vectors)),1000,10,0.1)
    #fig = plt.figure(constrained_layout=True)
    #gs = fig.add_gridspec(3,3)
    #for i in range(9):
    #    k = random.randint(0,len(y_train))
    #    x = x_train[k]
    #    y = y_train[k]
    #    plot = fig.add_subplot(gs[i//3,i%3])
    #    plot.imshow(np.reshape(x,(28,28)),cmap='gray')
    #    prediction = p.predict(x)
    #    res = 0
    #    mx = 0
    #    for j,pred in enumerate(prediction[0]):
    #        if pred>mx:
    #            mx = pred
    #            res = j
    #    plot.set_title("Predicted:"+str(res)+" Real:"+str(y))
    #    
    #plt.show()