from Pyro4 import expose, Future
import logging
import json
import subprocess
import sys
try:
    import numpy as np
    from PIL import Image
except:
    subprocess.call([sys.executable,"-m","pip","install","numpy"])
    subprocess.call([sys.executable,"-m","pip","install","Pillow"])
    import numpy as np
    from PIL import Image
    
input_format = ".txt"
output_format = ".txt"

color_map=[0, 0, 0,
            66, 45, 15,
            25, 7, 25,
            10, 0, 45,
            5, 5, 73,
            0, 7, 99,
            12, 43, 137,
            22, 81, 175,
            56, 124, 209,
            132, 181, 229,
            209, 234, 247,
            239, 232, 191,
            247, 201, 94,
            255, 170, 0,
            204, 127, 0,
            153, 86, 0,
            104, 51, 2]

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        log.info("Inited")

    def solve(self):
        log.info("Job Started")
        log.info("Workers %d" % len(self.workers))
        width,height = self.read_input()
        log.info("Picture "+str(width)+"x"+str(height))
        step = height // len(self.workers)

        # map
        mapped = []
        for i in range(len(self.workers)):
            #future = Future(self.workers[i].mymap)
            l = i*step
            r = (i+1)*step if (i+1)*step < height else height
            mapped.append(self.workers[i].mymap(l,r,width,height,color_map))

        log.info("Map finished")

        # reduce
        reduced = self.myreduce(mapped)
        log.info("Reduce finished")

        # output
        self.write_output(reduced)

        log.info("Job Finished")

    @staticmethod
    @expose
    def mymap(bottom, top, width, height,color_map):
        max_iterations = 1000
        res = []
        for y in range(bottom,top):
            row = []
            for x in range(width):
                cx = 3.5 * x / width - 2.5
                cy = 2.0 * y / height - 1.0
                zx = 0
                zy = 0
                iter = 0
                while iter < max_iterations:
                    tempzx = zx * zx - zy * zy + cx
                    zy = 2 * zx * zy + cy
                    zx = tempzx
                    if zx * zx + zy * zy > 4:
                        break
                    iter+=1
                pixel = [0, 0, 0]
                if iter != max_iterations:
                    map_id = (iter * 100 // max_iterations) % 17
                    pixel = color_map[map_id:map_id+3]
                row.append(pixel)
            res.append(row)
        return res

    @staticmethod
    @expose
    def myreduce(mapped):
        log.info("Reduce started")
        values = []
        for val in mapped:
            values.append(val.value)
        output = np.concatenate((values))
        return output

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            data = f.readline().split(' ')
        return int(data[0]),int(data[1])

    def write_output(self, output):
        img = Image.new("RGB",(len(output[0]),len(output)))
        data = img.load()
        for i in range(len(output)):
            for j in range(len(output[0])):
                data[j,i] = tuple(output[i][j])
        img.save(self.output_file_name)

log = logging.getLogger("Mandelbrot")

if __name__  == "__main__":
    t = (1,2,3)
    s = Solver()
    res1 = s.mymap(0,300,800,600)
    res2 = s.mymap(300,400,800,600)
    res3 = s.mymap(400,600,800,600)
    res = s.myreduce([res1,res2,res3])
    s.write_output(res)
