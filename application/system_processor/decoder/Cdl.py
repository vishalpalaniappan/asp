from pathlib import Path
from clp_ffi_py.ir import ClpIrFileReader
from decoder.CDL_CONSTANTS import LINE_TYPE
from decoder.CdlLogLine import CdlLogLine
from decoder.CdlHeader import CdlHeader

class Cdl:

    def __init__(self, fileName):
        '''
            Initialize the CDL reader.
        '''
        self.fileName = fileName
        self.header = None  

        self.execution = []
        self.exception = None
        self.traceEvents = {}
        self.callStack = []
        self.callStacks = {}

        self.loadAndParseFile(fileName)

    def loadAndParseFile(self, fileName):
        '''
            Load and parse the file line by line.
        '''
        with ClpIrFileReader(Path(fileName)) as clp_reader:
            for log_event in clp_reader:
                self.parseLogLine(log_event)

    def parseLogLine(self, log_event):
        '''
            Parse the log line and save the relevant data.
        '''
        currLog = CdlLogLine(log_event)

        if currLog.type == LINE_TYPE["IR_HEADER"]:
            self.header = CdlHeader(currLog.value)
        elif currLog.type == LINE_TYPE["EXCEPTION"]:
            self.exception = currLog.value
        elif currLog.type == LINE_TYPE["EXECUTION"]:
            self.execution.append(currLog)
            self.addToCallStack(currLog)
        elif currLog.type == LINE_TYPE["VARIABLE"]:
            self.execution.append(currLog)

    def addToCallStack(self, log):
        '''
            Add the current execution to the call stack.

            - If the log is a function, add it to stack.
            - Move down stack until parent function of current log is found
            - Map the stack positions to find the log which called the function
            - Add current position to stack
            - Copy stack into global list            
        '''
        position = len(self.execution) - 1
        ltInfo = self.header.getLtInfo(log.ltId)
        cs = self.callStack

        if (ltInfo.isFunction()):
            self.callStack.append(position)

        while (len(cs) > 0):
            currStackFuncLt = self.execution[cs[-1]].ltId
            if (int(currStackFuncLt) == int(ltInfo.getFuncLt())):
                break
            cs.pop()

        # Update the call stack to indicate where the functions were called from.
        csFromCallPosition = list(map(self.getPreviousPosition, self.callStack) )
        csFromCallPosition.append(position)

        self.callStacks[position] = csFromCallPosition
    
    def getPreviousPosition(self, position):
        '''
            Given a position, this function returns the previous execution
            log type. For example, when adding to the call stack, this will
            allow us to find the place where a function was called from.
        '''
        position -= 1
        while (position >= 0):
            if self.execution[position].type == LINE_TYPE["EXECUTION"]:
                return position
            position -= 1
        return position
        

if __name__ == "__main__":
    fileName = "../sample_system_logs/job_handler.clp.zst"
    f = Cdl(fileName)