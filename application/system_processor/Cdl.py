from application.system_processor.decoder.CdlDecoder import CdlDecoder
import os

class Cdl:

    def __init__(self, filePath):
        self.filePath = filePath
        self.logFileName = os.path.basename(filePath)
        self.decoder = CdlDecoder(filePath)

        self.decoder.getCallStackAtPosition(self.decoder.lastExecution)

    def uniqueTraceEvents(self):
        return self.decoder.uniqueTraceEvents
    
    def getFileTree(self):
        return self.decoder.header.fileTree

    def goToPosition(self, position):
        callStack = self.decoder.getCallStackAtPosition[position]
        return callStack

    def stepInto(self):
        pass

    def stepOut(self):
        pass

    def stepOverForward(self):
        pass
    
    def stepOverBackward(self):
        pass

    def goToStart(self):
        pass

    def goToEnd(self):
        pass