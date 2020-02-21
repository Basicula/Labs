from classifier import Classifier
from linear_regression import LinearRegression
from data_generator import DataGenerator
from utils import add_plot_model_predictions, add_plot_with_error_distrib, add_plot_data_2d

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
  fig = plt.figure(constrained_layout=True)
  gs = fig.add_gridspec(2,3)

  data, labels = DataGenerator.blobs_2d(100, 2)

  lg = LogisticRegression(learning_rate = 0.1, iterations = 1000)
  lg.fit(data, labels)
  
  sk_lg = LGR()
  sk_lg.fit(data, labels)
  
  N = 5000
  xs = np.random.rand(N,2)
  axis = (0,1,0,1)
  
  data_distrib = add_plot_data_2d(fig, gs[0,0], data, labels, "Data distribution", axis)
  
  res = add_plot_model_predictions(fig, gs[0,1], xs, lg, "Predictions", axis)
  
  sk_res = add_plot_model_predictions(fig, gs[0,2], xs, sk_lg, "sklearn predictions", axis)
  
  ys = lg.predict(xs, True)
  smooth = add_plot_data_2d(fig, gs[1,1], xs, ys, "Smooth predictions", axis)
  
  ys = sk_lg.predict_proba(xs)
  ys = np.array([max(1-y[0],y[1]) for y in ys])
  sk_smooth = add_plot_data_2d(fig, gs[1,2], xs, ys, "sklearn smooth predictions", axis)
  
  error = add_plot_with_error_distrib(fig, gs[1,0], lg.history)
  
  plt.show()
  

if __name__ == "__main__":
  test()