import os
import sys
import time
from cdl.Cdl import Cdl
from pathlib import Path
from database.EventWriter import EventWriter
from database.SystemWriter import SystemWriter
from assembler.TraceAssembler import TraceAssembler
from db import DBClient

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
        visitedFiles = set()
        self._continue_monitoring = True

        while self._continue_monitoring:
            try:
                time.sleep(2)
                current = set(os.listdir(self.logFolder))
                newFiles = current - visitedFiles

                if len(newFiles) == 0:
                    continue

                print("\nProcessing new files:")
                print(newFiles)

                for logFileName in newFiles:
                    if logFileName.endswith(".clp.zst"):
                        cdlFile = Cdl(os.path.join(self.logFolder, logFileName))
                        self.logFiles.append(cdlFile)
                        self.eventWriter.addEventsToDb(cdlFile)
                        self.sysWriter.write_file(cdlFile)

                # TODO: Only assemble the new nodes that were added
                TraceAssembler(self.db)

                visitedFiles = current
            except KeyboardInterrupt:
                print("Stopping monitoring...")
                self._continue_monitoring = False
            except Exception as e:
                print(f"Error in monitoring: {e}")

def main(argv):
    rootDir = Path(__file__).resolve().parents[0]
    
    isDocker = os.environ.get('IS_RUNNING_IN_DOCKER', False)

    if isDocker:
        SYSTEM_LOG_FILES = "/app/logs"
    else:
        SYSTEM_LOG_FILES = rootDir / "system_logs"

    processor = SystemProcessor(SYSTEM_LOG_FILES)
    processor.run()

if __name__ == "__main__":
    sys.exit(main(sys.argv))