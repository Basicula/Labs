import numpy as np
import matplotlib.pyplot as plt
from sklearn import naive_bayes

from data_generator import DataGenerator
from utils import add_plot_data_2d, add_plot_model_predictions

class GaussianBayesClassifier:
    def __init__(self):
        super().__init__();
    
    def prob(self, x, mean, variance):
        return 1/(np.sqrt(2*np.pi*variance)) * np.exp((-(x-mean)**2)/(2*variance))
        
    def fit(self, input, output):
        output = output.ravel()
        n = len(output)
        classes = np.unique(output)
        indices_by_class = np.zeros((len(classes), len(output)))
        self.probabilities = np.zeros(len(classes))
        self.means = np.zeros((len(classes), input.shape[1]))
        self.variances = np.zeros((len(classes), input.shape[1]))
        for c in classes:
            class_indices = output==c
            n_by_class = sum(class_indices)
            indices_by_class[c] = class_indices
            features_by_class = input[class_indices]
            
            self.probabilities[c] = n_by_class / n
            self.means[c] = np.mean(features_by_class, axis = 0)
            self.variances[c] = np.var(features_by_class, axis = 0)
    
    def predict(self,xs):
        predictions = np.zeros(len(xs))
        for k,x in enumerate(xs):
            n = len(self.probabilities)
            prediction = np.zeros(n)
            for i in range(n):
                prob = self.prob(x, self.means[i], self.variances[i])
                prediction[i] = self.probabilities[i] * np.prod(prob)
            predictions[k] = np.argmax(prediction)
        return predictions
    
    def error(self, input, output):
        pass

def test():
    data, labels = DataGenerator.blobs_2d(100,3)
    labels = labels.ravel()
    
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2,4)
    
    N = 1000
    axis = (0,1,0,1)
    
    data_distr = add_plot_data_2d(fig, gs[0,0], data, labels, "Data distribution", axis)
    
    xs = np.random.rand(N,2)
    bc = BayesClassifier()
    bc.fit(data, labels)
    
    res = add_plot_model_predictions(fig, gs[0,1], xs, bc, "Predictions", axis, True)
    
    sk_bc = naive_bayes.GaussianNB()
    sk_bc.fit(data, labels)
    
    sk_res = res = add_plot_model_predictions(fig, gs[1,1], xs, sk_bc, "sklearn predictions", axis, True)

    plt.show()

if __name__ == "__main__":
    test()