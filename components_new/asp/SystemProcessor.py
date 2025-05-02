import os
from cdl.Cdl import Cdl
from pathlib import Path
from database.EventWriter import EventWriter
from database.SystemWriter import SystemWriter
from assembler.TraceAssembler import TraceAssembler
from DbConn import DBClient

class SystemProcessor:

    def __init__(self, logFolder):
        '''
            Initialize the system processor with the logs from the given folder.
        '''
        self.logFolder = logFolder
        self.logFiles = []
        
        with DBClient() as db:
            # self.eventWriter = EventWriter(db)
            self.sysWriter = SystemWriter(db)
            self.parseSystemLogFiles()

        # Run the trace assembler on the events saved to the ioEvents database.
        # TraceAssembler()

    def parseSystemLogFiles(self):
        '''
            Parse the system log files contained in folder.
        '''
        files = os.listdir(self.logFolder)

        for logFileName in files:
            if logFileName.endswith(".clp.zst"):
                cdlFile = Cdl(os.path.join(self.logFolder, logFileName))
                self.logFiles.append(cdlFile)
                # self.eventWriter.addEventsToDb(cdlFile)
                self.sysWriter.write_file(cdlFile)

                # TraceAssembler()

if __name__ == "__main__":
    rootDir = Path(__file__).resolve().parents[0]
    SYSTEM_LOG_FILES = rootDir / "system_logs"
    processor = SystemProcessor(SYSTEM_LOG_FILES)