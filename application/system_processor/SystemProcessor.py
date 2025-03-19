import os
from decoder.Cdl import Cdl

class SystemProcessor:

    def __init__(self, logFolder):
        self.logFolder = logFolder
        self.parseLogFiles()
        self.logFiles = []

    def parseLogFiles(self):
        files = os.listdir(self.logFolder)

        for file in files:
            _path = os.path.join(self.logFolder, file)
            cdlFile = Cdl(_path)


if __name__ == "__main__":
    SYSTEM_LOG_FILES = "../sample_system_logs/"
    processor = SystemProcessor(SYSTEM_LOG_FILES)