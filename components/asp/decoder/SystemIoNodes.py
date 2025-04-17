class SystemIoNodes:
    '''
        This class accepts the system io nodes extracted while
        processing the CDL file. There are three types of nodes:

        Start Node: This is a node which has an output but no input.
        Link Node: This is a node which has an input and output.
        End Node: This is a node which has an input but no output.
    '''

    def __init__(self):
        self.classifiedNodes = []

    def processNodes(self, nodes):
        '''
            Process the provided nodes.
        '''
        for node in nodes:
            self.processNode(node)

        return self.classifiedNodes

    def processNode(self, node):
        '''
            Process the provided node.
        '''
        if "input" in node:
            return self.processInput(node["input"])        
        if "output" in node:
            return self.processOutput(node["output"])        

    def processInput(self, inputs):
        '''
            Process each input node.
        '''
        for input in inputs:
            if "output" in input:
                self.encodeLink(input)
            else:
                self.encodeEnd(input)

    def processOutput(self, outputs):
        '''
            Process each output node.
        '''
        for output in outputs:
            self.encodeStart(output)

    def encodeStart(self, startNode):
        '''
            Encode the start node.
        '''
        encodedStartNode = {
            "type": "start",
            "node": startNode
        }
        self.classifiedNodes.append(encodedStartNode)

    def encodeLink(self, linkNode):
        '''
            Encode the link node.
        '''
        encodedLinkNode = {
            "type": "link",
            "node": linkNode
        }
        self.classifiedNodes.append(encodedLinkNode)

    def encodeEnd(self, endNode):
        '''
            Encode the end node.
        '''
        encodedEndNode = {
            "type": "end",
            "node": endNode
        }
        self.classifiedNodes.append(encodedEndNode)