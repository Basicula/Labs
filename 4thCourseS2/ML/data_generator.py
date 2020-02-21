import numpy as np
import matplotlib.pyplot as plt

class DataGenerator:
  @staticmethod
  def random_2d(size, classes = 2):
    x = np.random.rand(size, 2)
    y = np.floor(np.random.rand(size, 1) * classes)
    return x, y
  
  @staticmethod
  def blobs_2d(blob_size, blob_cnt):
    x = np.zeros((blob_size * blob_cnt, 2))
    y = np.zeros((blob_size * blob_cnt, 1))
    id = 0
    for i in range(blob_cnt):
      center = np.random.rand(1, 2)
      for j in range(blob_size):
        r = (np.random.rand() - 0.5) * 0.25
        angle = np.random.rand() * 2 * np.pi
        x[id] = center + np.array([np.cos(angle), np.sin(angle)])*r
        y[id][0] = i
        id += 1
    return x, y
  
if __name__ == "__main__":
  gen = DataGenerator()
  x, y = gen.blobs_2d(100, 3)
  plt.scatter(*x.T, c = y.ravel())
  plt.axis((0,1,0,1))
  plt.show()
  