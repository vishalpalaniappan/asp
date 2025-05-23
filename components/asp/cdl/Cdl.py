from cdl.decoder.CdlDecoder import CdlDecoder
import os
import json

class Cdl:

    def __init__(self, filePath):
        self.filePath = filePath
        self.logFileName = os.path.basename(filePath)
        self.decoder = CdlDecoder(filePath)

        self.goToPosition(self.decoder.lastExecution)
    
    def getFileTree(self):
        return self.decoder.header.fileTree

    def goToPosition(self, position):
        '''
            Go to the given position
        '''
        callStack = self.decoder.getCallStackAtPosition(position)
        variables = self.decoder.getVariablesAtPosition(position)
        self.position = position
        return [callStack, variables]

    def stepInto(self, position):
        '''
            Step into the current position
        '''
        nextPosition = self.decoder.getNextExecutionPosition(position)
        if nextPosition:
            return self.goToPosition(nextPosition)
        
        return None

    def stepOut(self, position):
        '''
            Step out of the current position
        '''
        cs = self.decoder.callStacks[position]
        if len(cs) <= 1:
            return None
        return self.goToPosition(cs[-2])

    def stepOverForward(self, position):
        '''
            Step over function call forwards
        '''
        originalStackSize = len(self.decoder.callStacks[position])

        while position < len(self.decoder.execution):
            position = self.decoder.getNextExecutionPosition(position)

            if position is None:
                return None
            
            if len(self.decoder.callStacks[position]) <= originalStackSize:
                break
        
        return self.goToPosition(position)
    
    def stepOverBackward(self, position):
        '''
            Step over function calls backwards
        '''
        originalStackSize = len(self.decoder.callStacks[position])

        while position > 0:
            position = self.decoder.getPreviousExecutionPosition(position)

            if position is None:
                return None
            
            if len(self.decoder.callStacks[position]) <= originalStackSize:
                break
        
        return self.goToPosition(position)

    def goToStart(self):
        '''
            Go to the first executed line in the file.
        '''
        return self.goToPosition(0)

    def goToEnd(self):
        '''
            Go to the last executed line in the file.
        '''
        return self.goToPosition(self.decoder.lastExecution)