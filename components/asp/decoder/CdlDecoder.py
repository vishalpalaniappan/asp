from pathlib import Path
from clp_ffi_py.ir import ClpIrFileReader
from decoder.CDL_CONSTANTS import LINE_TYPE
from decoder.CdlLogLine import CdlLogLine
from decoder.CdlHeader import CdlHeader
from decoder.SystemIoNodes import SystemIoNodes

import os
import copy

class CdlDecoder:

    def __init__(self, filePath):
        '''
            Initialize the CDL reader.
        '''
        self.logFileName = os.path.basename(filePath)
        self.filePath = filePath
        self.header = None  

        self.execution = []
        self.exception = None
        self.callStack = []
        self.callStacks = {}

        self.nodes = []

        self.loadAndParseFile(filePath)

        self.systemIoNodes = SystemIoNodes().processNodes(self.nodes)

    def loadAndParseFile(self, filePath):
        '''
            Load and parse the file line by line.
        '''
        with ClpIrFileReader(Path(filePath)) as clp_reader:
            self.position = 0
            for log_event in clp_reader:
                self.parseLogLine(log_event)
        
        # Save any remaining system io nodes in the callstack
        while len(self.callStack) > 0:
            popped = self.callStack.pop()
            if (("input" in popped) or ("output" in popped)):
                self.nodes.append(popped)

    def parseLogLine(self, log_event):
        '''
            Parse the log line and process the relevant data.
        '''
        currLog = CdlLogLine(log_event)
        self.execution.append(currLog)

        if currLog.type == LINE_TYPE["JSON"]:
            self.processJSONLog(currLog)
        elif currLog.type == LINE_TYPE["EXCEPTION"]:
            self.exception = currLog.value
        elif currLog.type == LINE_TYPE["EXECUTION"]:
            self.lastExecution = self.position
            self.addToCallStack(currLog)
        elif currLog.type == LINE_TYPE["VARIABLE"]:
            pass
        
        self.position += 1


    def processJSONLog(self, log):
        '''
            This function processes any JSON logs.
        '''
        if (log.value["type"] == "adli_header"):
            self.header = CdlHeader(log.value["header"])
        elif (log.value["type"] == "adli_input"):
            self.processInput(log.value)
        elif (log.value["type"] == "adli_output"):
            self.processOutput(log.value)


    def processInput(self, logValue):
        '''
            Add the input to the top of the call stack.
        '''
        if "input" not in self.callStack[-1]:
            self.callStack[-1]["input"] = []
        self.callStack[-1]["input"].append(logValue)


    def processOutput(self, logValue):
        '''
            Process the output node.
            - Move down the stack
            - If an input was found, append the output to the input and return
            - If an input was not found, then append output to top of call stack
        '''
        for cs in reversed(self.callStack):
            if "input" in cs:
                if "output" not in cs["input"][-1]:
                    cs["input"][-1]["output"] = []
                cs["input"][-1]["output"].append(logValue)
                return
            
        if "output" not in self.callStack[-1]:
            self.callStack[-1]["output"] = []

        self.callStack[-1]["output"].append(logValue)

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
            self.callStack.append({"funcPosition":position})

        while (len(cs) > 0):
            currStackFuncLt = self.execution[cs[-1]["funcPosition"]].ltId
            if (int(currStackFuncLt) == int(ltInfo.getFuncLt())):
                break

            popped = cs.pop()

            # When the position is removed from the stack, add it to the
            # nodes list if the position has input or output information 
            # in it. The nodes will be processed in the next stage.
            if (("input" in popped) or ("output" in popped)):
                self.nodes.append(popped)
                
        # Update the call stack to indicate where the functions were called from.
        csFromCallPosition = []
        for cs in self.callStack:
            csFromCallPosition.append(self.getPreviousExecutionPosition(cs["funcPosition"]))
        csFromCallPosition.append(position)

        self.callStacks[position] = csFromCallPosition
    
    def getPreviousExecutionPosition(self, position):
        '''
            This function returns the previous execution position. 
            For example, when adding to the call stack, this will
            allow us to find the place where a function was called from.
        '''
        while (position >= 1):
            position -= 1
            if self.execution[position].type == LINE_TYPE["EXECUTION"]:
                return position
        return None

    def getNextExecutionPosition(self, position):
        '''
            This function returns the next execution position. 
        '''
        position += 1
        while (position < len(self.execution)):
            if self.execution[position].type == LINE_TYPE["EXECUTION"]:
                return position
            position += 1
        return None
    
    def getCallStackAtPosition(self, position):
        '''
            Get call stack info for the given position.
        '''
        csInfo = []
        for cs in self.callStacks[position]:
            lt = self.execution[cs].ltId
            ltInfo = self.header.getLtInfo(lt)
            funcLt = ltInfo.getFuncLt()

            if (funcLt == 0):
                funcName = "<module>"
            else:
                funcName = self.header.getLtInfo(funcLt).getName()

            csInfo.append({
                "functionName": funcName,
                "fileName": self.logFileName,
                "position": cs,
                "lineNumber": ltInfo.getLineNo()
            })

        return csInfo
    

    def updateVariable(self, variable, value, varStack, tempStack):
        '''
            Given a list of nested keys, this function creates the
            nested key tree and assigns the value on the last level.

            A key can can have three types:
            - variable : Load key from varStack
            - temp_variable : Load key from tempStack
            - value: Load from key["value"]
        '''
        name = variable.name

        if (len(variable.getKeys()) == 0):
            varStack[name] = value
            return

        currVal = {} if (name not in varStack) else copy.deepcopy(varStack[name])
        
        currLevel = currVal 
        for idx, key in enumerate(variable.getKeys()):
            newKey = key["value"]

            if (key["type"] == "temp_variable"):
                newKey = tempStack[newKey]
            elif (key["type"] == "variable"):
                newKey = varStack[newKey]

            if newKey not in currLevel or isinstance(currLevel[newKey], dict):
                currLevel[newKey] = {}

            # Assign value at last key, otherwise keep going down a level
            if idx + 1 == len(variable.getKeys()):
                currLevel[newKey] = copy.deepcopy(value)
            else:
                currLevel = currLevel[newKey]

        varStack[variable.name] = currVal
    
    def getVariablesAtPosition(self, position):
        '''
            Given a position, this function returns the variables 
            that are in the current and global scope.
        '''
        localVars = {}
        globalVars = {}
        tempVars = {}

        currLt = self.execution[position].ltId
        funcId = self.header.getLtInfo(currLt).getFuncLt()

        currPosition = 0
        while (currPosition < position):
            currLog = self.execution[currPosition]

            if currLog.type == LINE_TYPE["VARIABLE"]:
                variable = self.header.varMap[currLog.varId]
                varFuncId = variable.getFuncLt()

                if variable.isTempVar():
                    tempVars[variable.getName()] = currLog.value
                elif ((varFuncId == 0) or variable.isGlobal()):
                    self.updateVariable(variable, currLog.value, globalVars, tempVars)
                elif (varFuncId == funcId):
                    self.updateVariable(variable, currLog.value, localVars, tempVars)

            currPosition += 1

        return {
            "localVars" : localVars,
            "globalVars" : globalVars,
        }

    def getFunctionArgumentValues(self, position):
        '''
            This function returns the variable values of the given function's arguments.
            The arguments are logged after the function def, so we read the variables until
            the log isn't a variable, this will ensure that we save all the arguments.
        '''
        funcArgs = {}
        position += 1
        while position < len(self.execution) and (self.execution[position].type == LINE_TYPE["VARIABLE"]):
            varInfo = self.header.getVarInfo(self.execution[position].varId)
            funcArgs[varInfo.getName()] = self.execution[position].value
            position += 1

        return funcArgs