from Entity import _TextCollectionMetaPurpose as TextCollectionMetaPurpose

class TextCollectionMetaCommom(object):
    @staticmethod
    def CheckPurposesTestTrain(testTextCollectionMeta, trainTextCollectionMeta):
        TextCollectionMetaCommom.CheckPurpose(testTextCollectionMeta, TextCollectionMetaPurpose.test)
        TextCollectionMetaCommom.CheckPurpose(trainTextCollectionMeta, TextCollectionMetaPurpose.train)
    
    @staticmethod
    def CheckPurpose(textCollectionMeta, purpose):
        if(textCollectionMeta.purpose != purpose):
            errorMessage = " wrong purpose detected, please send a text-collection-meta with a " + purpose.name + "purpose"
            raise Exception(errorMessage)
