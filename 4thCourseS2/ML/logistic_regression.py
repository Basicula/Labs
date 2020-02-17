from classifier import Classifier
from linear_regression import LinearRegression

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression as LGR

def sigmoid(x):
  return 1 / (1 + np.exp(-x))

class LogisticRegression(Classifier):
  def __init__(self, learning_rate = 0.01, iterations = 1000):
      super().__init__(learning_rate, iterations)
      
  def fit(self, input, output):
      self.prefit(input, output)
      
      # z = x * W + b
      # y* = sigmoid(z) = sigmoid(x * W + b) = 1 / (1 + e^(-x * W - b))
      # loss function L(y*,y) = -y * log(y*) - (1 - y) * log(1 - y*)
      # dL/dy* = -y / y* + (1 - y) / (1 - y*)
      # dy*/dz = y* * (1 - y*) = sigmoid(z) * (1 - sigmoid(z))
      # dz/dW = x
      # dL/dW = dL/dy* * dy*/dz * dz/dW = (y* - y) * dz/dW = (y* - y) * x
      # dL/db = dL/dy* * dy*/dz * dz/db = (y* - y) * dz/db = y* - y
      for iter in range(self.iterations):
          predicted = self.predict(input, True)
          diff = predicted - output
          delta_w = input.T.dot(diff) / input.shape[0]
          delta_b = np.mean(diff)
          self.weights -= self.learning_rate * delta_w
          self.bias -= self.learning_rate * delta_b
          self.history[iter] = self.error(input, output)
          
  def predict(self, x, smooth = False):
      res = sigmoid(x.dot(self.weights) + self.bias)
      if smooth:
          return res
      else:
          temp = np.round(res)
          return temp
      
  #L(y*,y) = -y * log(y*) - (1 - y) * log(1 - y*)
  def error(self, input, output):
      predicted = self.predict(input, True)
      return np.sum(-output * np.log(predicted) - (1 - output) * np.log(1 - predicted)) / input.shape[0]

def test():
  np.random.seed(69)
  fig = plt.figure(constrained_layout=True)
  gs = fig.add_gridspec(2,3)
  
  def generate_data(cluster_size, dims):
      x = np.zeros((cluster_size * 2,dims))
      y = np.zeros((cluster_size * 2, 1))
      index = 0
      for j in range(2):
          center = np.random.rand(dims)
          for i in range(cluster_size):
              deltas = (np.random.rand(6,dims)-0.5)*0.8
              x[index] = min(deltas, key = np.linalg.norm)+center
              y[index][0] = j
              index+=1
      return x,y
  
  data, labels = generate_data(1000,2)

  lg = LogisticRegression(learning_rate = 0.1, iterations = 1000)
  lg.fit(data, labels)
  
  sk_lg = LGR()
  sk_lg.fit(data, labels)
  
  data_distrib = fig.add_subplot(gs[0,0])
  data_distrib.title.set_text("Data distribution")
  data_distrib.scatter(*data.T, c = labels.ravel())
  data_distrib.axis((0,1,0,1))

  N = 5000
  xs = np.random.rand(N,2)
  ys = lg.predict(xs)
  res = fig.add_subplot(gs[0,1])
  res.title.set_text("Predictions")
  res.scatter(*xs.T, c = ys.ravel())
  res.axis((0,1,0,1))
  
  ys = lg.predict(xs, True)
  smooth = fig.add_subplot(gs[1,1])
  smooth.title.set_text("Smooth predictions")
  smooth.scatter(*xs.T, c = ys.ravel())
  smooth.axis((0,1,0,1))
  
  ys = sk_lg.predict(xs)
  sk_res = fig.add_subplot(gs[0,2])
  sk_res.title.set_text("sklearn predictions")
  sk_res.scatter(*xs.T, c = ys)
  sk_res.axis((0,1,0,1))
  
  ys = sk_lg.predict_proba(xs)
  ys = [max(1-y[0],y[1]) for y in ys]
  sk_smooth = fig.add_subplot(gs[1,2])
  sk_smooth.title.set_text("sklearn smooth predictions")
  sk_smooth.scatter(*xs.T, c = ys)
  sk_smooth.axis((0,1,0,1))
  
  error = fig.add_subplot(gs[1,0])
  error.title.set_text("Error")
  x = np.arange(len(lg.history))
  y = lg.history
  error.plot(x,y)
  
  plt.show()
  

if __name__ == "__main__":
  test()