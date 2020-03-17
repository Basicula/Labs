from classifier import Classifier
from data_generator import DataGenerator
from utils import add_plot_data_2d, add_plot_model_predictions

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier as RFC

class Node:
    def __init__(self, root_feature, id, value, left = None, right = None):
        self.root_feature = root_feature
        self.id = id
        self.value = value
        self.left = left
        self.right = right

class RandomForestClassifier(Classifier):
    def __init__(self, max_depth = 10, n = 100, k = 10):
        super().__init__()
        self.forest = None
        self.max_depth = max_depth
        self.n_trees = n
        self.k = k

    def all_equal(self, output):
        return sum(output == output[0]) == len(output)

    def fit(self, input, output):
        self.forest = self.build_forest(input, output.ravel())

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
        id = np.random.randint(0, len(input[0]))
        all_features = input.T
        root_feature, min_entropy = self.find_best_split(all_features[id], output)
        return id, root_feature, min_entropy
    
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
    
    def build_forest(self, input, output):
        forest = []
        for i in range(self.n_trees):
            indices = np.random.choice(len(input), self.k)
            forest.append(self.build_tree(input[indices], output[indices]))
        return forest
    
    def predict_through_tree(self, node, x):
        while not node is None and not node.root_feature is None:
            if x[node.id] < node.root_feature:
                node = node.left
            else:
                node = node.right
        else:
            if not node is None:
                return node.value
        return -1
    
    def predict(self,xs):
        results = np.zeros(len(xs))
        for i, x in enumerate(xs):
            predictions = []
            for tree_root in self.forest:
                predictions.append(self.predict_through_tree(tree_root, x))
            results[i] = max(set(predictions), key=predictions.count)
        return results
        
    def error(self, input, output):
        pass

def test():     
    data, labels = DataGenerator.blobs_2d(100,5)
    
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2,2)
    
    N = 1000
    axis = (0,1,0,1)
    
    dtc = RandomForestClassifier(10)
    dtc.fit(data, labels)
    
    sk_dtc = RFC(max_depth = 10)
    sk_dtc.fit(data, labels)
    
    data_distr = add_plot_data_2d(fig, gs[0,0], data, labels, "Data distributions", axis)
    
    xs = np.random.rand(N,2)
    
    res = add_plot_model_predictions(fig, gs[0,1], xs, dtc, "Predictions", axis, True)

    sk_res = add_plot_model_predictions(fig, gs[1,1], xs, sk_dtc, "sklearn predictions", axis, True)

    plt.show()

if __name__ == "__main__":
    test()