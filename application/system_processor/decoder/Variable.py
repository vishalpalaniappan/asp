class Variable:
    '''
        This class stores and exposes information about a variable
    '''

    def __init__(self, varInfo):
        for key in varInfo:
            setattr(self, key, varInfo[key])

    def getName(self):
        return getattr(self, "name", None)
    
    def getFuncLt(self):
        return getattr(self, "funcid", None)
    
    def isTempVar(self):
        return getattr(self, "isTemp", None)
    
    def isGlobal(self):
        return getattr(self, "global", None)