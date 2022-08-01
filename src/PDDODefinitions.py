
class PDDOOperator:
    def __init__(self):
         self.numDiffOps = 0
         self.diffOps = 0
         self.norder = 0
         self.n1order = 0
         self.n2order = 0
         self.n3order = 0
         self.nsize = 0
         self.nskip = 0
         self.morder = 0
         self.asymFlag = 0
         self.numBC = 0
         self.BC = 0
         self.nteqs = 0
         self.ncons = 0
         self.aType = 0
         self.nout = 0
         self.numOut = 0
         self.nwk = 0

class Geometry:
    def __init__(self):
        self.totalNodes = 0
        self.coordinates = 0
        self.deltaVolumes = 0
        self.deltaCoordinates = 0
        self.nodeFamiliesIdx = 0
        self.boundaries = 0



