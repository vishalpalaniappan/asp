from decoder.CDL_CONSTANTS import LINE_TYPE_DELIMITER, LINE_TYPE
import json

class CdlLogLine:

    def __init__(self, log_event):
        self.timestamp = log_event.get_timestamp()

        # TODO: Improve the way this is implemented.
        line = log_event.get_log_message()[11:].strip()
        self.parseLine(line)

    def parseLine(self, line):
        '''
            Classify and parse the given log line.
        '''
        delimiter = line[0]
        
        if delimiter == LINE_TYPE_DELIMITER["JSON"]:
            self.parseJSONLog(line)
        elif delimiter == LINE_TYPE_DELIMITER["EXCEPTION"]:
            self.parseException(line)
        elif delimiter == LINE_TYPE_DELIMITER["VARIABLE"]:
            self.parseVariable(line)
        else:
            self.parseExecution(line)

    def parseJSONLog(self, line):
        '''
            Parse the IR stream JSON log.            
        '''
        self.type = LINE_TYPE["JSON"]
        self.value = json.loads(line)

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
        self.varId = int(split[1])
        self.value = self.parseIfJson("".join(split[2:]))

    def parseExecution(self, line):
        '''
            Parse Execution log statements
            "<logtypeid>"
        '''
        self.type = LINE_TYPE["EXECUTION"]
        self.ltId = int(line)


    def parseIfJson(self, value):
        '''
            Try parsing the variable as a json object.
            If it was unsuccessful, then return the value.
        '''
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value