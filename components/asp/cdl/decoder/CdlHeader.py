import json
from cdl.decoder.Variable import Variable
from cdl.decoder.LogType import LogType

class CdlHeader:

    def __init__(self, header):
        self.ltMap = {}
        self.varMap = {}
        self.saveHeaderInformation(header)

    def saveHeaderInformation(self, header):
        '''
            Save the header information while creating
            objects to store the variable and logtype
            information.
        '''
        self.fileTree = header["fileTree"]
        self.execInfo = header["execInfo"]
        self.programInfo = header["programInfo"]
        self.adliInfo = header["adliInfo"]
        self.sysinfo = header["sysInfo"]

        for lt in header["ltMap"]:
            self.ltMap[int(lt)] = LogType(header["ltMap"][lt])
        
        for lt in header["varMap"]:
            self.varMap[int(lt)] = Variable(header["varMap"][lt])


    def getLtInfo(self, logtype):
        '''
            Returns logtype info given a logtype id.
        '''
        return self.ltMap[logtype]
    
    def getVarInfo(self, varType):
        '''
            Returns variable info given a variable type.
        '''
        return self.varMap[varType]
    
    def getFileFromLt(self, lt):
        '''
            Returns the file that this logtype belongs to
        '''
        for file in self.fileTree:
            lt_value = int(lt)
            minLt = self.fileTree[file]["minLt"]
            maxLt = self.fileTree[file]["maxLt"]
            if (lt_value >= minLt and lt_value < maxLt):
                return file
            
        return None

