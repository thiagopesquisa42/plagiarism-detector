
from subprocess import check_call
import os

folderPath = 'C:\\Users\\thiagopesquisa42\\Desktop\\plagiarism-detector-optimus\\data\\experiment020p_tape003\\meta\\ResultsExport20180602_185217'

dotFileList = []
for _file in os.listdir(folderPath):
            if _file.endswith(".dot"):
                dotFileList.append(os.path.join(folderPath, _file))

dotExecutable = 'C:\\Program Files (x86)\\Graphviz2.38\\bin\\dot.exe'
for dotFile in dotFileList:
    check_call([dotExecutable,'-Tpng',dotFile,'-o', dotFile.split('.dot')[0] + '.png'])

