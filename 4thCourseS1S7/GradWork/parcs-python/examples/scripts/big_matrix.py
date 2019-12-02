import json
import numpy as np

def dump_matrix(n,file):
    res = {}
    res["left"] = (np.random.rand(n,n)*1000).tolist()
    res["right"] = (np.random.rand(n,n)*1000).tolist()
    with open(file,'w') as f:
        json.dump(res,f)
    
if __name__ == "__main__":
    dump_matrix(1000,"matrix1000x1000.txt")