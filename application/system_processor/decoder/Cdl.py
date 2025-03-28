from pathlib import Path
from clp_ffi_py.ir import ClpIrFileReader
from application.system_processor.decoder.CDL_CONSTANTS import LINE_TYPE
from application.system_processor.decoder.CdlLogLine import CdlLogLine
from application.system_processor.decoder.CdlHeader import CdlHeader

class Cdl:

    def __init__(self, logFileName, filePath):
        '''
            Initialize the CDL reader.
        '''
        self.logFileName = logFileName
        self.filePath = filePath
        self.header = None  

        self.execution = []
        self.exception = None
        self.uniqueTraceEvents = {}
        self.callStack = []
        self.callStacks = {}

        self.loadAndParseFile(filePath)

    def loadAndParseFile(self, filePath):
        '''
            Load and parse the file line by line.
        '''
        with ClpIrFileReader(Path(filePath)) as clp_reader:
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
            self.saveUniqueId(currLog)

    def saveUniqueId(self, variable):
        '''
            Save the asp_uid variable value to the top of the stack.
        '''
        varInfo = self.header.getVarInfo(variable.varId)

        if varInfo.getName() == "asp_uid":
            self.callStack[-1]["uid"] = variable.value

    def addUniqueTrace(self, uid, startPos, endPos):
        '''
            Given a start and end position of a unique trace, 
            add the position and level of each function in the
            trace to the unique trace object.
        '''

        # Add every visited function and its level in the stack to the trace list 
        trace = []
        for position in range(startPos, endPos):
            lineType = self.execution[position]

            if lineType.type == LINE_TYPE["EXECUTION"]:
                ltInfo = self.header.getLtInfo(lineType.ltId)

                if (ltInfo.isFunction()):
                    trace.append({
                        "position": position,
                        "level": len(self.callStacks[position]),
                        "name": ltInfo.getName(),
                        "lineNo": ltInfo.lineno,
                        "file": self.header.getFileFromLt(ltInfo.id)
                    })

        # Add trace to the unique traceEvents list.
        if uid not in self.uniqueTraceEvents:
            self.uniqueTraceEvents[uid] = []        
        
        self.uniqueTraceEvents[uid].append({
            "programName": self.logFileName.split(".")[0] + ".py",
            "trace": trace,
            "timestamp": self.execution[startPos].timestamp
        })

    def addToCallStack(self, log):
        '''
            Add the current execution to the call stack.

            - If the log is a function, add it to stack.
            - Move down stack until parent function of current log is found
            - Map the stack positions to find the log which called the function
            - Add current position to stack
            - Copy stack into global list            

            - If a unique trace function is added to stack, it is the start of a unique trace.
            - If a unique trace function is removed from stack, it is the end of a unique trace.
            - When a unique trace ends, save it to the unique trace list.
        '''
        position = len(self.execution) - 1
        ltInfo = self.header.getLtInfo(log.ltId)
        cs = self.callStack

        if (ltInfo.isFunction()):
            self.callStack.append({"position":position,"isUnique":ltInfo.isUnique})

        while (len(cs) > 0):
            currStackFuncLt = self.execution[cs[-1]["position"]].ltId
            if (int(currStackFuncLt) == int(ltInfo.getFuncLt())):
                break

            popped = cs.pop()

            # If the removed call is the end of a unique trace, then add it to the trace list.
            if popped["isUnique"]:
                self.addUniqueTrace(popped["uid"], popped["position"], position)
                
        # Update the call stack to indicate where the functions were called from.
        csFromCallPosition = list(map(self.getPreviousExecutionPosition, self.callStack))
        csFromCallPosition.append(position)

        self.callStacks[position] = csFromCallPosition
    
    def getPreviousExecutionPosition(self, cs):
        '''
            Given a position, this function returns the previous execution
            log type. For example, when adding to the call stack, this will
            allow us to find the place where a function was called from.
        '''
        position = cs["position"]
        position -= 1
        while (position >= 0):
            if self.execution[position].type == LINE_TYPE["EXECUTION"]:
                return position
            position -= 1
        return position
        

if __name__ == "__main__":
    fileName = "../sample_system_logs/job_handler.clp.zst"
    f = Cdl(fileName)