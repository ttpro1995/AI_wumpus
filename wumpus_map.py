import copy
class MapReader:
    """ Read a text file which is map for wumpus game
        the text file is this

        (wall is wrap outside)
        The map represent the part inside the wall

        0 1 2 0
        0 0 0 3

        1: pit
        2: wumpus
        3: gold
    """
    def __init__(self):
        self.width = 0
        self.height = 0
        self.matrix = []

    def read(self,fname):
        f = open(fname)
        self.height = self.file_len(fname)

        i = 0;
        j = 0;
        for line in f:
            line_m = []
            line = line.rstrip('\n')
            words = line.split()
            for w in words:
                self.width = len(w)
                num = int(w)
                line_m.append(num)
        self.matrix.append(copy.deepcopy(line_m))
        self.height = len(self.matrix)

    def getMap(self):


        return self.matrix

    def file_len(self,fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        self.height = i+1
        a = open(fname)
        lines = a.readline()
        print(lines)
        self.width = len(lines.split())
        print("height ", str(self.height))
        print("wid ", str(self.width))


# test

m = MapReader()
filename="wumpus_map.txt"
print(m.file_len(filename))