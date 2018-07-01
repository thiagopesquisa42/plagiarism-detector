
class ResultsExport():
    def __init__(self,
        classifierMeta):
        fileMetaList = [
            FileMeta(content = classifierMeta.report, prefix = 'classifier', suffix = '.report'),
            FileMeta(content = classifierMeta.definitionDictionary, prefix = 'classifier', suffix = '.configuration'),
            FileMeta(content = classifierMeta.graphviz, prefix = 'graphviz', suffix = '.dot'),
            FileMeta(content = classifierMeta.summaryTrainData, prefix = 'trainData', suffix = '.summary'),
            FileMeta(content = classifierMeta.summaryTestData, prefix = 'testData', suffix = '.summary'),
            FileMeta(content = classifierMeta.attributesReport, prefix = 'classifierAttributes', suffix = '.report')]
        self.fileMetaList = fileMetaList
        self.nickname = classifierMeta.GetName()

class FileMeta():
    def __init__(self, content, prefix, suffix = '.txt'):
        if(not isinstance(prefix, str) or not isinstance(suffix, str)):
            raise TypeError('prefix and suffix must be strings.')
        if(not '.' in suffix):
            suffix = '.'+ suffix
        self.prefix = prefix
        self.suffix = suffix
        self.content = content
