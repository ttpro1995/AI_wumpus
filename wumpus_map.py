import copy
import numpy
class MapReader:
    """ Read a text file which is map for wumpus game
        the text file is this

        (wall is wrap outside)
        The map represent the part inside the wall

        0 1 2 0
        0 0 0 3

        1: pit
        2: wumpus (only one wumpus)
        3: gold (only one gold)
    """
    def __init__(self, fname):
        self.width = 0
        self.height = 0
        self.fname = fname
        self.file_len(fname)
        self.read_map()
        self.transpose_map()

    def read_map(self):
        fname = self.fname
        f = open(fname).read()
        self.matrix = numpy.zeros(shape=(self.height, self.width))
        lines = f.splitlines()
        for i in range(self.height):
            a_line = lines[i]
            words = a_line.split()
            for j in range(self.width):
                self.matrix[i,j] = words[j]



    def getMap(self):


        return self.matrix

    def file_len(self,fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        self.height = i+1
        a = open(fname)
        lines = a.readline()

        self.width = len(lines.split())


    def transpose_map(self):
        tmp = self.width
        self.width = self.height
        self.height = tmp
        self.matrix.transpose()



# test
filename="wumpus_map.txt"
m = MapReader(filename)

m.getMap()