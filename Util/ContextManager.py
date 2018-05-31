from constant import ContextDefaultFolders, Contexts
import os

class ContextManager():
    global experimentLocation
    experimentLocation = ''

    def InitExperiment(experimentUniqueName):
        ContextManager._SetExperimentLocation(experimentUniqueName)
        ContextManager._CheckUniqueExperimentName()
        return ContextManager._GetExperimentLocation()

    def _CheckUniqueExperimentName():
        experimentLocation = ContextManager._GetExperimentLocation()
        if(experimentLocation == ContextDefaultFolders.ROOT_FOLDER):
            raise Exception('Invalid experiment location:' + str(experimentLocation))
        if(os.path.exists(experimentLocation)):
            raise Exception('There is an experiment with the same name previously.')

    def ContinueExperiment(experimentUniqueName):
        ContextManager._SetExperimentLocation(experimentUniqueName)
        experimentLocation = ContextManager._GetExperimentLocation()
        if(not os.path.exists(experimentLocation)):
            raise Exception('This experiment doesn\'t exist: ' + str(experimentLocation))
        return ContextManager._GetExperimentLocation()

    def _SetExperimentLocation(experimentUniqueName):
        global experimentLocation
        experimentLocation = os.path.join(
            ContextDefaultFolders.ROOT_FOLDER, experimentUniqueName)
    
    def _GetExperimentLocation():
        global experimentLocation
        return experimentLocation
    
    def GetContextLocation(context):
        subFolder = ContextManager._MapperContextToSubFolder(context)
        contextLocation = ContextManager._GetContextLocationBySubFolder(subFolder)
        return contextLocation

    def _MapperContextToSubFolder(context):
        if(context == Contexts.TRAIN):
            return ContextDefaultFolders.Experiment.Data.TRAINING_SUBFOLDER
        if(context == Contexts.TEST):
            return ContextDefaultFolders.Experiment.Data.TESTING_SUBFOLDER
        if(context == Contexts.CLASSIFIER):
            return ContextDefaultFolders.Experiment.Data.CLASSIFIER_SUBFOLDER
        if(context == Contexts.META):
            return ContextDefaultFolders.Experiment.Data.META_SUBFOLDER
        raise Exception('unknown context!')

    def _GetContextLocationBySubFolder(subFolderName):
        return os.path.join(ContextManager._GetExperimentLocation(), subFolderName)