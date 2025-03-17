from pathlib import Path
from clp_ffi_py.ir import ClpIrFileReader
import json

class CDL:

    LINE_TYPE = {
        "VARIABLE": 1,
        "EXCEPTION": 2,
        "EXECUTION": 3,
        "IR_HEADER": 4,
    }

    LINE_TYPE_DELIMITER = {
        "VARIABLE": "#",
        "EXCEPTION": "?",
        "IR_HEADER": "{",
    }

    def __init__(self, fileName):
        '''
            Initialize the CDL reader.
        '''
        self.header = None
        self.execution = []
        self.exception = None

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
        delimiter = line[0]

        if delimiter == CDL.LINE_TYPE_DELIMITER["IR_HEADER"]:
            self.header = json.loads(line)
        elif delimiter == CDL.LINE_TYPE_DELIMITER["EXCEPTION"]:
            self.exception = line
        elif delimiter == CDL.LINE_TYPE_DELIMITER["VARIABLE"]:
            self.exception = line
        else:
            self.execution.append(line)


if __name__ == "__main__":
    f = CDL("test.clp.zst")