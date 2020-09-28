from keras.models import Model
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing.image import img_to_array, load_img
import matplotlib.pyplot as plt
import numpy as np

example_root = 'example16/'

def nearest_sqr(n):
    sqrt_n = int(np.sqrt(n))
    if sqrt_n * sqrt_n == n:
        return sqrt_n
    return sqrt_n + 1

def get_filters_for_layer(model, layer_id):
    if layer_id >= len(model.layers):
        return []

    filters, biases = model.layers[layer_id].get_weights()
    
    f_min, f_max = filters.min(), filters.max()
    filters = (filters - f_min) / (f_max - f_min)
    return filters
    
def prepare_for_visualization(filters_shape, max_n_filters = None):
    n_filters = filters_shape[3]
    if not max_n_filters is None:
        n_filters = min(n_filters, max_n_filters)
    n = nearest_sqr(n_filters)
    
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(n,n)
    return fig, gs, n_filters, n
    
def visualize_layer_filters_separately_rgb(filters, max_n_filters = None):
    n_filters = filters.shape[3]
    if not max_n_filters is None:
        n_filters = min(n_filters, max_n_filters)
    n = nearest_sqr(n_filters)
    
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(n,3*n)

    for i in range(n_filters):
        filter = filters[:, :, :, i]
        for j in range(3):
            ax = fig.add_subplot(gs[i // n, 3 * (i % n) + j])
            if j == 0:
                ax.title.set_text("Red")
            elif j == 1:
                ax.title.set_text("Green")
            elif j == 2:
                ax.title.set_text("Blue")
            ax.set_xticks([])
            ax.set_yticks([])
            plt.imshow(filter[:, :, j], cmap='gray')
    plt.savefig(example_root + 'separately_rgb.png')

def visualize_layer_filters_rgb(filters, max_n_filters = None):
    fig, gs, n_filters, n = prepare_for_visualization(filters.shape, max_n_filters)

    for i in range(n_filters):
        filter = filters[:, :, :, i]
        ax = fig.add_subplot(gs[i // n, i % n])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.imshow(filter[:, :])
    
    plt.savefig(example_root + 'rgb.png')
    
def visualize_picture():
    fig = plt.figure(constrained_layout=True)
    ax = fig.add_subplot()
    
    img = load_img('picture.jpg', target_size=(224, 224))
    ax.imshow(img)
    
def visualize_feature_map_block_by_block(model, custom_indices = None, feature_size = None):
    indices = np.arange(len(model.layers))
    if not custom_indices is None:
        indices = custom_indices
    outputs = []
    names = []
    for layer_id in indices:
        layer = model.layers[layer_id]
        if 'block' in layer.name:
            outputs.append(layer.output)
            names.append(layer.name)
    model = Model(inputs=model.inputs, outputs=outputs)
    
    img = load_img('picture.jpg', target_size=(224, 224))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    feature_maps = model.predict(img)
    
    for i, feature_map in enumerate(feature_maps):
        fig = plt.figure(constrained_layout=True)
        #fig.suptitle('Feature map after layer ' + names[i], fontsize=16)
        if feature_size is None:
            feature_size = feature_map.shape[3]
        n = nearest_sqr(feature_size)
        gs = fig.add_gridspec(n, n)
        for feature_id in range(feature_size):
            ax = fig.add_subplot(gs[feature_id // n, feature_id % n])
            ax.set_xticks([])
            ax.set_yticks([])
            ax.imshow(feature_map[0, :, :, feature_id])
        plt.savefig(example_root + 'feature_map_' + names[i] + '.png')

def main():
    model = VGG16()
    
    n = 16
    filters = get_filters_for_layer(model, 1)
    visualize_layer_filters_separately_rgb(filters, n)
    visualize_layer_filters_rgb(filters, n)
    visualize_picture()
    visualize_feature_map_block_by_block(model, feature_size = n)
    
    #plt.show()

if __name__ == "__main__":
    main()