import json
import os
from pathlib import Path 

class TraceAssembler:
    '''
        This class assembles all the system io nodes 
        that were identified while parsing the CDL file.

        It starts at the start nodes, then it follows the 
        chain of link nodes and end at an end node. 

        start -> link -> link -> end
    '''

    def __init__(self, system):
        self.logs = []
        self.traces = []
        self.system = system
        self.currentTrace = []

    def processLogs(self):
        '''
            Process all system log files.
        '''
        for log in self.system.logFiles:
            self.processLog(log)

        with open("traces.json","w+") as f:
            f.write(json.dumps(self.traces))
        return self.traces
    
    def processLog(self, log):
        '''
            For each identified event, check if it is a start node.
            If it is, find the place where this output is an input. 
        '''
        for ioEvent in log.decoder.systemIoNodes:
            if ioEvent["type"] == "start":
                self.currentTrace = []
                # self.currentTrace.append(ioEvent["node"])
                self.currentTrace.append(log.decoder.header.programInfo["name"])
                self.findTrace(ioEvent["node"])
                self.traces.append(self.currentTrace)

    def findTrace(self, searchNode):
        '''
            Search for the given node, specified by its searchId
            and searchIndex.
        '''
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
                            self.currentTrace.append(log.decoder.header.programInfo["name"])
                            # TODO: Add support for processing multiple outputs.
                            self.findTrace(node["output"][0])
                        else:
                            self.currentTrace.append(log.decoder.header.programInfo["name"])