import os
from application.system_processor.decoder.Cdl import Cdl
import json

class SystemProcessor:

    def __init__(self, logFolder):
        '''
            Initialize the system processor with the logs from the given folder.
        '''
        self.logFolder = logFolder
        self.logFiles = []
        self.uniqueTraces = {}

        self.parseSystemLogFiles()

    def parseSystemLogFiles(self):
        '''
            Parse the system log files contained in folder.
        '''
        files = os.listdir(self.logFolder)

        for file in files:
            if file.endswith(".clp.zst"):
                _path = os.path.join(self.logFolder, file)
                cdlFile = Cdl(_path)
                self.addUniqueTraceEvents(cdlFile.uniqueTraceEvents)
                self.logFiles.append(cdlFile)
        
        # Sort the trace events by timestamp
        for uid in self.uniqueTraces:
            self.uniqueTraces[uid].sort(key=lambda x: x["timestamp"], reverse=False)

        # Save trace events to json file
        with open("traceEvents.json", "w+") as f:
            f.write(json.dumps(self.uniqueTraces))

    def addUniqueTraceEvents(self, traceEvents):
        '''
            Add trace events from log files to system unique trace list.
        '''
        for traceUid in traceEvents:            
            if traceUid not in self.uniqueTraces:
                self.uniqueTraces[traceUid] = []

            self.uniqueTraces[traceUid] += traceEvents[traceUid]

    def getFileTrees(self):
        '''
            Returns the file tree for all programs in the system
        '''
        fileTrees = {}
        for log in self.logFiles:
            fileTrees[log.fileName] = log.header.fileTree

        return fileTrees

if __name__ == "__main__":
    SYSTEM_LOG_FILES = "../sample_system_logs/"
    processor = SystemProcessor(SYSTEM_LOG_FILES)