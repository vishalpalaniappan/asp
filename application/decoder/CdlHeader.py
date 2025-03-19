import json
from Variable import Variable
from LogType import LogType

class CdlHeader:

    def __init__(self, headerJsonString):
        self.ltMap = {}
        self.varMap = {}
        self.saveHeaderInformation(headerJsonString)

    def saveHeaderInformation(self, headerJsonString):
        '''
            Save the header information while creating
            objects to store the variable and logtype
            information.
        '''
        header = json.loads(headerJsonString)

        self.fileTree = header["fileTree"]

        for lt in header["ltMap"]:
            self.ltMap[lt] = LogType(header["ltMap"][lt])
        
        for lt in header["varMap"]:
            self.varMap[lt] = Variable(header["varMap"][lt])


