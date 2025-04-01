from application.system_processor.decoder.CdlDecoder import CdlDecoder
import os

class Cdl:

    def __init__(self, filePath):
        self.logFileName = os.path.basename(filePath)
        self.decoder = CdlDecoder(filePath)
    