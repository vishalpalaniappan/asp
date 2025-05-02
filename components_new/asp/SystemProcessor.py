import os
import sys
import time
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

    def run(self):
        with DBClient() as db:
            self.db = db
            self.eventWriter = EventWriter(db)
            self.sysWriter = SystemWriter(db)
            self.monitorFolder()


    def monitorFolder(self):
        '''
            Parse the system log files contained in folder.
        '''
        visitedFiles = []

        while True:
            time.sleep(2)
            current = os.listdir(self.logFolder)
            newFiles = current - visitedFiles

            if len(newFiles) == 0:
                continue

            for logFileName in newFiles:
                if logFileName.endswith(".clp.zst"):
                    cdlFile = Cdl(os.path.join(self.logFolder, logFileName))
                    self.logFiles.append(cdlFile)
                    self.eventWriter.addEventsToDb(cdlFile)
                    self.sysWriter.write_file(cdlFile)

            # TODO: Only assemble the new nodes that were added
            TraceAssembler(self.db)
            
            visitedFiles = current


def main(argv):
    rootDir = Path(__file__).resolve().parents[0]
    SYSTEM_LOG_FILES = rootDir / "system_logs"
    processor = SystemProcessor(SYSTEM_LOG_FILES)
    processor.run()

if __name__ == "__main__":
    sys.exit(main(sys.argv))