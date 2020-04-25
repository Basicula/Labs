import sys
import os
import numpy as np

def generate_matrix(filename, height, width, bottom, top):
    with open(filename, 'w') as f:
        f.write(str(height) + " " + str(width) + "\n")
        for i in range(height):
            for j in range(width):
                f.write(str(np.random.randint(bottom, top)) + " ")
            f.write("\n")

if __name__ == "__main__":
    generate_matrix(sys.argv[1], 
        int(sys.argv[2]), 
        int(sys.argv[3]), 
        int(sys.argv[4]), 
        int(sys.argv[5]))