from application.system_processor.decoder.CdlDecoder import CdlDecoder
import os

class Cdl:

    def __init__(self, filePath):
        self.filePath = filePath
        self.logFileName = os.path.basename(filePath)
        self.decoder = CdlDecoder(filePath)

        self.goToPosition(self.decoder.lastExecution)

        self.stepOverBackward(self.decoder.lastExecution)

    def uniqueTraceEvents(self):
        '''
            Return the unique traces in the log file
        '''
        return self.decoder.uniqueTraceEvents
    
    def getFileTree(self):
        return self.decoder.header.fileTree

    def goToPosition(self, position):
        '''
            Go to the given position
        '''
        callStack = self.decoder.getCallStackAtPosition(position)
        print(callStack)
        return callStack

    def stepInto(self, position):
        '''
            Step into the current position
        '''
        nextPosition = self.decoder.getNextExecutionPosition(position)
        self.goToPosition(nextPosition)

    def stepOut(self, position):
        '''
            Step out of the current position
        '''
        cs = self.decoder.callStacks[position]
        if len(cs) <= 1:
            return
        self.goToPosition(cs[-2])

    def stepOverForward(self, position):
        '''
            Step over function call forwards
        '''
        originalStackSize = len(self.decoder.callStacks[position])

        while position < len(self.decoder.execution):
            position = self.decoder.getNextExecutionPosition(position)

            if position == None:
                return
            
            if len(self.decoder.callStacks[position]) <= originalStackSize:
                break
        
        self.goToPosition(position)
    
    def stepOverBackward(self, position):
        '''
            Step over function calls backwards
        '''
        originalStackSize = len(self.decoder.callStacks[position])

        while position < len(self.decoder.execution):
            position = self.decoder.getPreviousExecutionPosition(position)

            if position == None:
                return
            
            if len(self.decoder.callStacks[position]) <= originalStackSize:
                break
        
        self.goToPosition(position)

    def goToStart(self):
        '''
            Go to the first executed line in the file.
        '''
        self.goToPosition(0)

    def goToEnd(self):
        '''
            Go to the last executed line in the file.
        '''
        self.goToPosition(self.decoder.lastExecution)