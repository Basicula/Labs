from classifier import Classifier
from utils import add_plot_model_predictions, add_plot_data_2d, add_plot_with_roc_curve
from data_generator import DataGenerator, split_data

import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier as DTClassifier

class Node:
    def __init__(self, root_feature, id, value, left = None, right = None):
        self.root_feature = root_feature
        self.id = id
        self.value = value
        self.left = left
        self.right = right

class DecisionTreeClassifier(Classifier):
    def __init__(self, max_depth = 10):
        super().__init__()
        self.root = None
        self.max_depth = max_depth
        
    def entropy_func(self,class_count, n):
        if class_count == 0:
            return 0
        return -(class_count / n) * np.log2(class_count / n)
        
    def get_entropy_for_group(self, group):
        n = len(group)
        classes = set(group)
        group_entropy = 0
        for c in classes:
            n_c = sum(group==c)
            if n_c == 0 or n_c == n:
                entropy = 0
            else:
                entropy = n_c * (self.entropy_func(n_c, n) + self.entropy_func(n - n_c, n))
            group_entropy += entropy/n
        return group_entropy
        
    def get_entropy(self, division, real):
        left = real[division]
        left_entropy = self.get_entropy_for_group(left)
        n_left = len(left)
        
        right = real[~division]
        right_entropy = self.get_entropy_for_group(right)
        n_right = len(right)
        
        n = n_right + n_left
        
        split_entropy = n_left / n * left_entropy + n_right / n * right_entropy
        return split_entropy
    
    def find_best_split(self, feature_list, output):
        n = len(feature_list)
        min_entropy = np.inf
        root_feature = None
        for feature_val in set(feature_list):
            predictions = feature_list < feature_val
            entropy = self.get_entropy(predictions, output)
            if entropy <= min_entropy:
                min_entropy = entropy
                root_feature = feature_val
        return root_feature, min_entropy
        
    def split(self, input, output):
        id = None
        min_entropy = np.inf
        root_feature = None
        all_features = input.T
        for i, c in enumerate(all_features):
            cur_feature, entropy = self.find_best_split(c, output)
            if entropy == 0:
                return i, cur_feature, entropy
            elif entropy <= min_entropy:
                min_entropy = entropy
                id = i
                root_feature = cur_feature
        return id, root_feature, min_entropy
        
    def all_equal(self, output):
        return sum(output == output[0]) == len(output)
        
    def build_tree(self, input, output, depth = 0):
        if len(output) == 0:
            return None
        elif self.all_equal(output):
            return Node(None, None, output[0])
        elif depth >= self.max_depth:
            return Node(None, None, np.round(np.mean(output)))
        id, root_feature, entropy = self.split(input, output)
        value = np.round(np.mean(output))
        node = Node(root_feature, id, value)
        output_left = output[input[:, id] < root_feature]
        output_right = output[input[:, id] >= root_feature]
        node.left = self.build_tree(input[input[:, id] < root_feature], output_left, depth + 1)
        node.right = self.build_tree(input[input[:, id] >= root_feature], output_right, depth + 1)
        return node
        
    def fit(self, input, output):
        self.root = self.build_tree(input, output.ravel())
    
    def predict_through_tree(self, x):
        node = self.root
        while not node is None and not node.root_feature is None:
            if x[node.id] < node.root_feature:
                node = node.left
            else:
                node = node.right
        else:
            if not node is None:
                return node.value
        return -1
    
    def predict(self, x):
        results = np.zeros(len(x))
        for i, c in enumerate(x):
            results[i] = self.predict_through_tree(c)
        return results
        
    def error(self, input, output):
        pass


def test():     
    data, labels = DataGenerator.blobs_2d(1000,3)
    trainX, trainY, testX, testY = split_data(data, labels)
    
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2,3)
    
    N = 1000
    axis = (0,1,0,1)
    
    dtc = DecisionTreeClassifier(10)
    dtc.fit(trainX, trainY)
    
    sk_dtc = DTClassifier(max_depth = 10)
    sk_dtc.fit(trainX, trainY)
    
    data_distr = add_plot_data_2d(fig, gs[0,0], data, labels, "Data distributions", axis)
    
    #xs = np.random.rand(N,2)
    
    res = add_plot_model_predictions(fig, gs[0,1], testX, dtc, "Predictions", axis, True)

    sk_res = add_plot_model_predictions(fig, gs[1,1], testX, sk_dtc, "sklearn predictions", axis, True)
    
    add_plot_with_roc_curve(fig, gs[0,2], testY, dtc.predict(testX))
    add_plot_with_roc_curve(fig, gs[1,2], testY, sk_dtc.predict(testX))

    plt.show()

if __name__ == "__main__":
    test()
    