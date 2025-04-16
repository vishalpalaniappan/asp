import json
from decoder.CDL_CONSTANTS import LINE_TYPE

class NodeProcessor():

    def __init__(self, decoder):
        '''
            Initialize the node processor.

            :param CdlDecoder decoder: A CdlDecoder instance which is processing its nodes.
        
        '''
        self.decoder = decoder
        self.classifiedNodes = []
        

    def classifyNodes(self):
        for node in self.decoder.nodes:
            if "input" in node:
                for input in node["input"]:
                    if "output" in input:
                        self.processLinkNode(node)
                    else:
                        self.processEndNode(node)
            
            if "output" in node:
                for output in node["output"]:
                    self.processStartNode(node)
                    
        return self.classifiedNodes


    def getLtInfoFromPosition(self, position):
        lt = self.decoder.execution[position].ltId
        ltInfo = self.decoder.header.getLtInfo(lt)
        return ltInfo.__dict__

    def processStartNode(self, node):
        funcPosition = node["funcPosition"]
        stmtPosition = node["output"][0]["adliExecutionIndex"]-1
        self.classifiedNodes.append({
            "type": "start",
            "node": node,
            "funcLtInfo": self.getLtInfoFromPosition(funcPosition),
            "ltInfo": self.getLtInfoFromPosition(stmtPosition)
        })

    def processEndNode(self, node):
        funcPosition = node["funcPosition"]
        stmtPosition = node["input"][0]["adliExecutionIndex"]-1

        self.classifiedNodes.append({
            "type": "end",
            "node": node,
            "funcLtInfo": self.getLtInfoFromPosition(funcPosition),
            "ltInfo": self.getLtInfoFromPosition(stmtPosition)
        })

    def processLinkNode(self, node):
        position = node["funcPosition"]
        endPosition = node["input"][0]["output"][0]["adliExecutionIndex"]
        stack = []

        while(position < endPosition):
            log = self.decoder.execution[position]

            if log.type == LINE_TYPE["EXECUTION"]:
                ltInfo = self.decoder.header.getLtInfo(log.ltId)
                if(ltInfo.isFunction()):
                    stack.append(ltInfo.__dict__)

            position += 1

        self.classifiedNodes.append({
            "type": "link",
            "node": node,
            "stack": stack
        })