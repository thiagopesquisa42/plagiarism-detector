
class ExperimentMeta():
    def __init__(self,
        classifierMeta):
        report = {
            'classifier-test-report': classifierMeta.report,
            'classifier-definition': classifierMeta.definitionDictionary
        }
        self.report = report
