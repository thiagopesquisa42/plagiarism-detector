
class SeedAttributes():
    def __init__(self):
        self.plagiarismClass             = None
        self.percentualInDetection       = None
        
        self.cosine                      = None
        self.dice                        = None
        
        self.isMaxCosine                 = None
        self.maxCosineDiff               = None
        self.meanMaxCosineDiff           = None
        self.maxCosineNeighbour          = None
        self.verticalCosineMaxDistance   = None
        self.verticalCosineMaxMeasure    = None

        self.isMaxDice                   = None
        self.maxDiceDiff                 = None
        self.meanMaxDiceDiff             = None
        self.maxDiceNeighbour            = None
        self.verticalDiceMaxDistance     = None
        self.verticalDiceMaxMeasure      = None

        self.lengthRatio                 = None
