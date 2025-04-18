import os
from Cdl import Cdl
from pathlib import Path
from EventWriter import EventWriter

class SystemProcessor:

    def __init__(self, logFolder):
        '''
            Initialize the system processor with the logs from the given folder.
        '''
        self.logFolder = logFolder
        self.logFiles = []
        self.eventWriter = EventWriter()
        self.parseSystemLogFiles()


    def parseSystemLogFiles(self):
        '''
            Parse the system log files contained in folder.
        '''
        files = os.listdir(self.logFolder)

        for logFileName in files:
            if logFileName.endswith(".clp.zst"):
                cdlFile = Cdl(os.path.join(self.logFolder, logFileName))
                self.logFiles.append(cdlFile)
                self.eventWriter.addEventsToDb(cdlFile)

if __name__ == "__main__":
    rootDir = Path(__file__).resolve().parents[0]
    SYSTEM_LOG_FILES = rootDir / "sample_system_logs"
    processor = SystemProcessor(SYSTEM_LOG_FILES)