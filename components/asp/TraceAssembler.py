import json

class TraceAssembler:

    def __init__(self, system):
        self.logs = []
        self.traces = []
        self.system = system
        self.currentTrace = []

    def processLogs(self):
        for log in self.system.logFiles:
            print("")
            print(log.decoder.header.programInfo)
            self.processLog(log)
        return self.traces
    
    def processLog(self, log):
        for ioEvent in log.decoder.systemIoNodes:
            if ioEvent["type"] == "start":
                print("")
                print(log.decoder.header.programInfo["name"])
                self.currentTrace = []
                self.currentTrace.append(ioEvent["node"])
                self.findTrace(ioEvent["node"])
                self.traces.append(self.currentTrace)

    def findTrace(self, searchNode):
        id = searchNode["adliExecutionId"]
        index = searchNode["adliExecutionIndex"]

        for log in self.system.logFiles:

            for ioEvent in log.decoder.systemIoNodes:
                
                if ioEvent["type"] == "link" or ioEvent["type"] == "end":
                    node = ioEvent["node"]
                    nodeId = node["adliExecutionId"]
                    nodeIndex = node["adliExecutionIndex"]

                    if ((id == nodeId) and (index == nodeIndex)):
                        if "output" not in node:
                            print(log.decoder.header.programInfo["name"])
                            self.currentTrace.append(node)
                        else:
                            print(log.decoder.header.programInfo["name"])
                            self.currentTrace.append(node)
                            self.findTrace(node["output"][0])