from pathlib import Path
from clp_ffi_py.ir import ClpIrFileReader
from CDL_CONSTANTS import LINE_TYPE_DELIMITER, LINE_TYPE
from CdlLogLine import CdlLogLine
import json
from Variable import Variable
from CdlHeader import CdlHeader

class Cdl:

    def __init__(self, fileName):
        '''
            Initialize the CDL reader.
        '''
        self.header = None  

        self.execution = []
        self.exception = None
        self.uniqueids = []

        self.loadAndParseFile(fileName)

    def loadAndParseFile(self, fileName):
        '''
            Load and parse the file line by line.
        '''
        with ClpIrFileReader(Path(fileName)) as clp_reader:
            for log_event in clp_reader:
                line = log_event.get_log_message()[11:].rstrip()
                self.parseLogLine(line)


    def parseLogLine(self, line):
        '''
            Parse the log line and save the relevant data.
        '''
        currLog = CdlLogLine(line)

        if currLog.type == LINE_TYPE["IR_HEADER"]:
            self.header = CdlHeader(currLog.value)
        elif currLog.type == LINE_TYPE["EXCEPTION"]:
            self.exception = currLog.value
        elif currLog.type == LINE_TYPE["EXECUTION"]:
            self.execution.append(currLog)
        elif currLog.type == LINE_TYPE["UNIQUE_ID"]:
            self.execution.append(currLog)
        elif currLog.type == LINE_TYPE["VARIABLE"]:
            self.execution.append(currLog)

if __name__ == "__main__":
    fileName = "../sample_system_logs/job_handler.clp.zst"
    f = Cdl(fileName)