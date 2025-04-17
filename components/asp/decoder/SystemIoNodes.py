

class SystemIoNodes:

    def __init__(self):
        self.classifiedNodes = []

    def processNodes(self, nodes):
        for node in nodes:
            self.processNode(node)

    def processNode(self, node):
        if "input" in node:
            return self.processInput(node["input"])        
        if "output" in node:
            return self.processOutput(node["output"])        

    def processInput(self, inputs):
        for input in inputs:
            if "output" in input:
                self.encodeLink(input)
            else:
                self.encodeEnd(input)


    def processOutput(self, outputs):
        for output in outputs:
            self.encodeStart(output)


    def encodeStart(self, startNode):
        print("Start Node.")
        encodedStartNode = {
            "type": "start",
            "node": startNode
        }
        self.classifiedNodes.append(encodedStartNode)

    def encodeLink(self, linkNode):
        print("Link Node.")
        encodedLinkNode = {
            "type": "link",
            "node": linkNode
        }
        self.classifiedNodes.append(encodedLinkNode)


    def encodeEnd(self, endNode):
        print("End Node.")
        encodedEndNode = {
            "type": "end",
            "node": endNode
        }
        self.classifiedNodes.append(encodedEndNode)