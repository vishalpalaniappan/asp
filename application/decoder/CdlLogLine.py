from CDL_CONSTANTS import LINE_TYPE_DELIMITER, LINE_TYPE
import json

class CdlLogLine:

    def __init__(self, line):
        line = line.strip()
        self.parseLine(line)

    def parseLine(self, line):
        '''
            Classify and parse the given log line.
        '''
        delimiter = line[0]
        
        if delimiter == LINE_TYPE_DELIMITER["IR_HEADER"]:
            self.parseHeader(line)
        elif delimiter == LINE_TYPE_DELIMITER["EXCEPTION"]:
            self.parseException(line)
        elif delimiter == LINE_TYPE_DELIMITER["VARIABLE"]:
            self.parseVariable(line)
        elif delimiter == LINE_TYPE_DELIMITER["UNIQUE_ID"]:
            self.parseUniqueId(line)
        else:
            self.parseExecution(line)

    def parseHeader(self, line):
        '''
            Parse the IR stream header            
        '''
        self.type = LINE_TYPE["IR_HEADER"]
        self.value = line
        pass

    def parseException(self, line):
        '''
            Parse exception log statements
            "? <Exception>"
        '''
        split = line.split()

        self.type = LINE_TYPE["EXCEPTION"]
        self.value = "".join(split[1:])
        pass

    def parseVariable(self, line):
        '''
            Parse variable log statements
            "# <var_id> <var_value>"
        '''
        split = line.split()

        self.type = LINE_TYPE["VARIABLE"]
        self.varId = split[1]
        self.value = self.parseIfJson("".join(split[2:]))

    def parseUniqueId(self, line):
        '''
            Parse unique id log statements
            "@ [start|end] <unique_id>"
        '''
        split = line.split()

        self.type = LINE_TYPE["UNIQUE_ID"]
        self.traceEvent = split[1]
        self.uid = self.parseIfJson("".join(split[2:]))

    def parseExecution(self, line):
        '''
            Parse Execution log statements
            "<logtypeid>"
        '''
        self.type = LINE_TYPE["EXECUTION"]
        self.ltId = line


    def parseIfJson(self, value):
        '''
            Try parsing the variable as a json object.
            If it was unsuccessful, then return the value.
        '''
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value