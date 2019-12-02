from Pyro4 import expose
import logging

class ConsoleLog:
    def __init__(self):
        pass
        
    def info(self,text):
        print(text)

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        log.info("Inited")

    def solve(self):
        log.info("Job Started")
        log.info("Workers %d" % len(self.workers))
        n = self.read_input()
        step = n / len(self.workers)

        # map
        mapped = []
        for i in xrange(0, len(self.workers)):
            log.info("Add range ["+str(i * step)+","+str(i * step + step)+"]")
            mapped.append(self.workers[i].mymap(i * step, i * step + step))

        log.info("Map finished:")

        # reduce
        reduced = self.myreduce(mapped)
        log.info("Reduce finished: " + str(reduced))

        # output
        self.write_output(reduced)

        log.info("Job Finished")

    @staticmethod
    @expose
    def mymap(a, b):
        log.info("Add range ["+str(a)+","+str(b)+"]")
        res = 0
        for i in xrange(a, b):
            res += i
        log.info("Range result:"+str(res))
        return res

    @staticmethod
    @expose
    def myreduce(mapped):
        output = 0
        for x in mapped:
            output += x.value
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()

log = logging.getLogger("Adder Solver")
