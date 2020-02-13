from classifier import Classifier
import numpy as np
import matplotlib.pyplot as plt

# fits to equation y = kx + b
class LinearRegression(Classifier):
    def __init__(self, learning_rate = 0.01, iterations = 1000):
        super().__init__(learning_rate, iterations)

    # preffered input and output as numpy arrays
    def fit(self, input, output):
        self.prefit(input, output)
        
        for iter in range(self.iterations):
            predicted = self.predict(input)
            #loss = (predicted - output) ** 2
            #gradient descent
            delta_w = 2 * input.T.dot(predicted - output) / input.shape[0]
            delta_b = 2 * np.mean(predicted - output, axis = 0)
            self.weights -= delta_w * self.learning_rate
            self.bias -= delta_b * self.learning_rate
            self.history[iter] = self.error(input, output)
        
    def predict(self, x):
        return x.dot(self.weights) + self.bias
        
    # MSE Mean Squared Error
    def error(self, input, output):
        predicted = input.dot(self.weights) + self.bias
        return np.sum((predicted - output)**2) / input.shape[0]
        
def random_color_hex():
    return "#" + ("%06x" % np.random.randint(0, 0xffffff))

def common_test(test_cnt):
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2,2)
    
    data_distr = fig.add_subplot(gs[0,0])
    data_distr.title.set_text("Data distribution")
    
    predictions = fig.add_subplot(gs[0,1])
    predictions.title.set_text("Predictions")
    
    main = fig.add_subplot(gs[1,0])
    main.title.set_text("All together")
    
    history = fig.add_subplot(gs[1,1])
    history.title.set_text("Error")
    
    avarage_history = None
    for test in range(test_cnt):
        k = np.random.rand() * 5 - 3
        b = np.random.rand() * 5
        x = np.arange(0,10,0.1).reshape(-1,1)
        y = np.vectorize(lambda x: x * k + b + np.random.rand())(x).reshape(-1,1)
        lr = LinearRegression()
        lr.fit(x,y)
        if avarage_history is None:
            avarage_history = lr.history
        else:
            avarage_history += lr.history
        y_predict = lr.predict(x)
        data_color = random_color_hex()
        main.scatter(x, y, label = 'data', c = data_color)
        data_distr.scatter(x, y, c = data_color)
        prediction_color = random_color_hex()
        main.plot(x, y_predict, label = 'prediction', c = prediction_color)
        predictions.plot(x, y_predict, c = prediction_color)
    
    main.legend()
    avarage_history /= test_cnt
    history.plot(np.arange(0,len(avarage_history)), avarage_history)
    plt.show()

if __name__ == "__main__":
    common_test(5)