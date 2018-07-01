

import os

mainFolder = 'data\\experiment005p_tape011_multiClass_randomSample\\panDetections\\mine'
folders = [x[0] for x in os.walk(mainFolder)]
for filesFolderPath in folders: 
    xmlFilesNames = []
    for _file in os.listdir(filesFolderPath):
        if _file.endswith(".xml"):
            xmlFilesNames.append(_file)
    count = 0
    for filePath in xmlFilesNames:
        with open(os.path.join(filesFolderPath, filePath), 'r') as _file:
            text = _file.read()
            count += len(text.split('feature')) - 1

    print(str(filesFolderPath) + ': ' + str(count))





