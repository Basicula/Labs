import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist
import random
import json
from threading import Thread
import time

def sigmoid(x):
    return 1/(1+np.exp(-x))
    
def sigmoid_prime(x):
    return sigmoid(x)*(1-sigmoid(x))

class Perceptron:
    def __init__(self,layer_sizes,name="Default"):
        self.name = name
        self.num_layers = len(layer_sizes)
        self.layer_sizes = layer_sizes
        self.biases = [np.random.randn(1,x) for x in self.layer_sizes[1:]]
        self.weights = [np.random.randn(x,y) for x,y in zip(self.layer_sizes,self.layer_sizes[1:])]
        self.errors = []
        
    def predict(self,input):
        out = input
        for w,b in zip(self.weights,self.biases):
            out = sigmoid(np.dot(out,w) + b)
        return out
        
    """ SGD - stochastic gradient descent """
    def trainSGD(self,training_data,epochs,mini_batch_size,learning_rate):
        print("Training starts")
        for i in range(epochs):
            start = time.time()
            random.shuffle(training_data)
            self.error = 0
            threads = []
            for k in range(0,len(training_data),mini_batch_size):
                mini_batch = training_data[k:min(k+mini_batch_size,len(training_data)-1)]
                
                threads.append(Thread(target=self.update_coefs,args=(mini_batch,)))
                threads[-1].start()
            
            for j in range(len(threads)):
                threads[j].join()
            
            self.errors.append(self.error)
            finish = time.time()
            dt = (finish - start)*1000
            message = "Progress:" + str(100*(i+1)/epochs) + "% in "
            for d,t in zip([1000,60,60,60],["ms","s","m","h"]):
                if dt < d:
                    message += str(dt) + t
                    break
                else:
                    dt /= d
            print(message)
                
    def update_coefs(self, batch):
        db_sum, dw_sum, err = self.update_batch(batch)
        self.error += err
        
        self.weights = [w+dw/len(batch) for w,dw in zip(self.weights,dw_sum)]
        self.biases = [b+db/len(batch) for b,db in zip(self.biases,db_sum)]
                
    def update_batch(self,batch):
        db_sum = [np.zeros(b.shape) for b in self.biases]
        dw_sum = [np.zeros(w.shape) for w in self.weights]
        error = 0
        for x,y in batch:
            db,dw,err = self.backpropagation(x,y)
            error+=err
            for j in range(len(db_sum)):
                db_sum[j] += db[j]
                dw_sum[j] += dw[j]
        
        return db_sum, dw_sum, error           
                
    def backpropagation(self,x,y):
        db = [np.zeros(b.shape) for b in self.biases]
        dw = [np.zeros(w.shape) for w in self.weights]
        
        activations = [x]
        results = []
        for b,w in zip(self.biases,self.weights):
            result = np.dot(activations[-1],w) + b
            results.append(result)
            activations.append(sigmoid(result))
            
        error = y-activations[-1]
        
        dloss = 2*error*sigmoid_prime(results[-1])
        db[-1] = dloss
        dw[-1] = activations[-2].T.dot(dloss)
        for i in range(2,self.num_layers):
            dloss = dloss.dot(self.weights[-i+1].T)*sigmoid_prime(results[-i])
            db[-i] = dloss
            dw[-i] = activations[-i-1].T.dot(dloss)
        return db,dw,error.mean()**2
        
    def save(self):
        weights = []
        for w in self.weights:
            weights.append(w.tolist())
        biases = []
        for b in self.biases:
            biases.append(b.tolist())
        with open(self.name+"_coefs.txt","w") as file:
            json.dump({"weight" : weights,"biases" : biases,"errors":self.errors},file)  

    def load(self,filename):
        with open(filename,"r") as file:
            data = json.load(file)
            self.weights = []
            for w in data['weight']:
                self.weights.append(np.array(w))
            self.biases = []
            for b in data['biases']:
                self.biases.append(np.array(b))
            self.errors = data['errors']
        
def test():
    x = [np.reshape(i,(1,2)) for i in np.array([[0,0],[0,1],[1,0],[1,1]])]
    y = np.array([0,1,1,0]).T
    p = Perceptron([2,4,1],"XoR")
    p.trainSGD(list(zip(x,y)),2500,2,1)
    print(p.predict(np.reshape(np.array([0,0]),(1,2))))
    print(p.predict(np.reshape(np.array([1,0]),(1,2))))
    print(p.predict(np.reshape(np.array([0,1]),(1,2))))
    print(p.predict(np.reshape(np.array([1,1]),(1,2))))
    plt.plot(range(len(p.errors)),p.errors)
    plt.show()
        
if __name__=="__main__":
    from google.colab import files
    files.download('digit_recognition.nn')