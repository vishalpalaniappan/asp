import json

class TraceAssembler:

    def __init__(self, system):
        self.logs = []
        self.traces = []
        self.system = system

    def processLogs(self):
        for log in self.system.logFiles:
            print("")
            print(log.decoder.header.programInfo)
            self.processLog(log)
        return self.traces
    
    def processLog(self, log):
        for ioEvent in log.decoder.systemIoNodes:
            if ioEvent["type"] == "start":
                print("start")
                self.findTrace(ioEvent["node"])

    def findTrace(self, node):
        id = node["adliExecutionId"]
        index = node["adliExecutionIndex"]

        for log in self.system.logFiles:
            self.checkLog(log, id , index)

    def checkLog(self, log, id , index):
        for node in log.decoder.systemIoNodes:
            nodeId = node["node"]["adliExecutionId"]
            nodeIndex = node["node"]["adliExecutionIndex"]

            if ((id == nodeId) and (index == nodeIndex)):
                print("FOUND MATCH")

    
    