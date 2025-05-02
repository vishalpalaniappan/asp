class LogType:
    '''
        This class stores and exposes information about a log type.
    '''

    def __init__(self, ltInfo):
        for key in ltInfo:
            setattr(self, key, ltInfo[key])

    def getLt(self):
        return getattr(self, "id", None)
    
    def getFuncLt(self):
        return getattr(self, "funcid", None)
    
    def getType(self):
        return getattr(self, "type", None)

    def isFunction(self):
        return getattr(self, "type", None) == "function"
    
    def isUnique(self):
        return getattr(self, "isUnique", None)
    
    def getLineNo(self):
        return getattr(self, "lineno", None)
        
    def getName(self):
        return getattr(self, "name", None)
