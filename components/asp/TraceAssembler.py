import json
import os
from pathlib import Path 

class TraceAssembler:

    def __init__(self, system):
        self.logs = []
        self.traces = []
        self.system = system
        self.currentTrace = []

    def processLogs(self):
        for log in self.system.logFiles:
            self.processLog(log)
        return self.traces
    
    def processLog(self, log):
        for ioEvent in log.decoder.systemIoNodes:
            if ioEvent["type"] == "start":
                self.currentTrace = []
                self.currentTrace.append(ioEvent["node"])
                self.findTrace(ioEvent["node"])
                self.traces.append(self.currentTrace)

    def findTrace(self, searchNode):
        searchId = searchNode["adliExecutionId"]
        searchIndex = searchNode["adliExecutionIndex"]

        for log in self.system.logFiles:
            fileName = log.logFileName.split(".")[0]
            for ioEvent in log.decoder.systemIoNodes:
                
                if ioEvent["type"] == "link" or ioEvent["type"] == "end":
                    node = ioEvent["node"]
                    currId = node["adliExecutionId"]
                    currIndex = node["adliExecutionIndex"]

                    if ((searchId == currId) and (searchIndex == currIndex)):
                        if "output" in node:
                            self.currentTrace.append(node)
                            # TODO: Add support for processing multiple outputs.
                            self.findTrace(node["output"][0])
                        else:
                            self.currentTrace.append(node)