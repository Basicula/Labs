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
        
    @staticmethod
    def curvelike_2d(curve_size, curve_cnt):
        x = np.zeros((curve_size * curve_cnt, 2))
        y = np.zeros((curve_size * curve_cnt, 1))
        id = 0
        for i in range(curve_cnt):
            curve_length = np.random.randint(50, 100)
            curve_points = np.zeros((curve_length, 2))
            for j in range(curve_length):
                point = np.random.rand(2)
                if j > 1:
                    dir = curve_points[j-2] - curve_points[j-1]
                    point = curve_points[j-1] + ((point - 0.25) * 1.75 + dir) * np.random.rand() * 0.05
                elif j > 0:
                    point = curve_points[j-1] + ((point - 0.25) * 0.05)
                curve_points[j] = point
            #plt.plot(*curve_points.T)
            for j in range(curve_size):
                point_id = np.random.randint(0,curve_length)
                to_prev = np.array([0,0]) if point_id == 0 else curve_points[point_id] - curve_points[point_id-1]
                to_next = np.array([0,0]) if point_id == curve_length - 1 else curve_points[point_id] - curve_points[point_id+1]
                noise = ((np.random.rand(2) - 0.5) * 0.25)
                x[id] = curve_points[point_id] + np.random.rand() * to_prev + np.random.rand() * to_next + 0.25 * noise
                y[id][0] = i
                id += 1
        return x, y
  
if __name__ == "__main__":
  gen = DataGenerator()
  x, y = gen.curvelike_2d(100, 2)
  plt.scatter(*x.T, c = y.ravel())
  #plt.axis((0,1,0,1))
  plt.show()
  