from pathlib import Path
from clp_ffi_py.ir import ClpIrFileReader
from CDL_CONSTANTS import LINE_TYPE_DELIMITER, LINE_TYPE
import json

class CDL:

    def __init__(self, fileName):
        '''
            Initialize the CDL reader.
        '''
        self.header = None
        self.execution = []
        self.exception = None

        self.loadAndParseFile(fileName)

        print(self.execution)


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
        delimiter = line[0]

        if delimiter == LINE_TYPE_DELIMITER["IR_HEADER"]:
            self.header = json.loads(line)
        elif delimiter == LINE_TYPE_DELIMITER["EXCEPTION"]:
            self.exception = line
        elif delimiter == LINE_TYPE_DELIMITER["VARIABLE"]:
            pass
        elif delimiter == LINE_TYPE_DELIMITER["UNIQUE_ID"]:
            pass
        else:
            self.execution.append(line)


if __name__ == "__main__":
    fileName = "../sample_system_logs/job_handler.clp.zst"
    f = CDL(fileName)