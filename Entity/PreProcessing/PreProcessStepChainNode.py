
class PreProcessStepChainNode():
    def __init__(self,
        preProcessedData,       
        preProcessStep,
        stepPosition,
        previousPreProcessStepChainNode = None):
        self.preProcessedData = preProcessedData
        self.preProcessStep = preProcessStep
        self.stepPosition = stepPosition
        self.previousPreProcessStepChainNode = previousPreProcessStepChainNode
