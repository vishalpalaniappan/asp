import json

class TraceAssembler:

    def __init__(self, system):
        self.logs = []
        self.traces = []
        self.system = system
        self.currentTrace = []

    def processLogs(self):
        for log in self.system.logFiles:
            # print(log.decoder.header.programInfo)
            self.processLog(log)
        return self.traces
    
    def processLog(self, log):
        for ioEvent in log.decoder.systemIoNodes:
            if ioEvent["type"] == "start":
                print("")
                print("-------start----------")
                print(ioEvent["node"]["adliValue"])
                print("----------------------")
                print(log.decoder.header.programInfo["name"])
                self.currentTrace = []
                self.currentTrace.append(ioEvent["node"])
                self.findTrace(ioEvent["node"])
                self.traces.append(self.currentTrace)

    def findTrace(self, searchNode):
        searchId = searchNode["adliExecutionId"]
        searchIndex = searchNode["adliExecutionIndex"]

        for log in self.system.logFiles:

            for ioEvent in log.decoder.systemIoNodes:
                
                if ioEvent["type"] == "link" or ioEvent["type"] == "end":
                    node = ioEvent["node"]
                    currId = node["adliExecutionId"]
                    currIndex = node["adliExecutionIndex"]

                    if ((searchId == currId) and (searchIndex == currIndex)):
                        if "output" not in node:
                            print(log.decoder.header.programInfo["name"])
                            print("--------end-----------")
                            print(ioEvent["node"]["adliValue"])
                            print("----------------------")
                            self.currentTrace.append(node)
                        else:
                            print(log.decoder.header.programInfo["name"])
                            self.currentTrace.append(node)
                            self.findTrace(node["output"][0])