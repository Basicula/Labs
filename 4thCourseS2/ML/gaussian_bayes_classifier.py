import numpy as np
import matplotlib.pyplot as plt
from sklearn import naive_bayes

from data_generator import DataGenerator, split_data
from utils import add_plot_data_2d, add_plot_model_predictions, add_plot_with_roc_curve

class GaussianBayesClassifier:
    def __init__(self):
        super().__init__();
    
    def prob(self, x, mean, variance):
        return 1/(np.sqrt(2*np.pi*variance)) * np.exp((-(x-mean)**2)/(2*variance))
        
    def fit(self, input, output):
        output = output.ravel()
        n = len(output)
        classes = np.unique(output)
        self.class_cnt = len(classes)
        indices_by_class = np.zeros((self.class_cnt, len(output)))
        self.probabilities = np.zeros(self.class_cnt)
        self.means = np.zeros((self.class_cnt, input.shape[1]))
        self.variances = np.zeros((self.class_cnt, input.shape[1]))
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
    
    def predict_proba(self, xs):
        predictions = np.zeros((len(xs), self.class_cnt))
        for k,x in enumerate(xs):
            prediction = np.zeros(self.class_cnt)
            for i in range(self.class_cnt):
                prob = self.prob(x, self.means[i], self.variances[i])
                prediction[i] = self.probabilities[i] * np.prod(prob)
            predictions[k] = prediction
        return predictions
    
    def error(self, input, output):
        pass

def test_with_roc(classes = 2):
    data, labels = DataGenerator.blobs_with_noise_2d(100,classes,classes * 5)
    labels = labels.ravel()
    trainX, trainY, testX, testY = split_data(data, labels)
    
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2,2+classes)
    
    axis = (0,1,0,1)
    
    data_distr = add_plot_data_2d(fig, gs[0,0], data, labels, "Data distribution", axis)
    
    bc = GaussianBayesClassifier()
    bc.fit(trainX, trainY)
    
    res = add_plot_model_predictions(fig, gs[0,1], testX, bc, "Predictions", axis, True)
    
    sk_bc = naive_bayes.GaussianNB()
    sk_bc.fit(trainX, trainY)
    
    sk_res = res = add_plot_model_predictions(fig, gs[1,1], testX, sk_bc, "sklearn predictions", axis, True)
    
    for c in range(classes):
        add_plot_with_roc_curve(fig, gs[0,2+c], testY==c, bc.predict_proba(testX)[:,c], "ROC for class " + str(c))
        add_plot_with_roc_curve(fig, gs[1,2+c], testY==c, sk_bc.predict_proba(testX)[:,c], "sklearn ROC for class " + str(c))

    plt.show()

def test(classes=2):
    data, labels = DataGenerator.blobs_2d(100,classes)
    labels = labels.ravel()
    
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2,2)
    
    N = 1000
    axis = (0,1,0,1)
    
    data_distr = add_plot_data_2d(fig, gs[0,0], data, labels, "Data distribution", axis)
    
    xs = np.random.rand(N,2)
    bc = GaussianBayesClassifier()
    bc.fit(data, labels)
    
    res = add_plot_model_predictions(fig, gs[0,1], xs, bc, "Predictions", axis, True)
    
    sk_bc = naive_bayes.GaussianNB()
    sk_bc.fit(data, labels)
    
    sk_res = res = add_plot_model_predictions(fig, gs[1,1], xs, sk_bc, "sklearn predictions", axis, True)

    plt.show()

if __name__ == "__main__":
    test(5)
    test_with_roc(4)