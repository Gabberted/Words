import inspect

class C(object):
    def __init__(self, strMessage,gDebugLevel):
        self._Message = strMessage
        _iLevel=0
        _gDebugLevel=gDebugLevel
    @property
    def Message(self):
        """I'm the 'x' property."""
        return self._Message
    def ilevel(self):
        return self._iLevel
    def gDebugLevel(self):
        return self._gDebugLevel


    @Message.setter
    def Message(self, value):
        self._Message = value

    def iLevel(self,value):
        self._iLevel=value

    def gDebugLevel(self,value):
        self._gDebugLevel=value

    @Message.deleter
    def Message(self):
        del self._Message

    def iLevel(self):
        del self._iLevel

    def gDebugLevel(self):
        del self._gDebugLevel


    def print(self,strMessage):
        try:
            #print("debug: " + strMessage)
            #iLevel=self.iLevel
            boDebugPrint=False
            iLevel=1
            #gDebugLevel=int(self.gDebugLevel().toString())
            gDebugLevel=2
            #print("gDebugLevel: " + str(gDebugLevel))
            if strMessage=="Entering":
                iLevel=int(iLevel)+1
                boDebugPrint=True
            if strMessage=="Leaving":
                boDebugPrint=True

            strTab=""
            if int(gDebugLevel)>1:
                for i in range(int(iLevel)):
                    #print(str(i))
                    strTab=strTab + "\t"
                    if boDebugPrint == True:
                        print("debug (" + str(iLevel) + ") : " + strTab + inspect.stack()[1][3] + " -> "  + strMessage)
                    else:
                        print("Message (" + str(iLevel) + ") : " + strTab + " -> "  + strMessage)
            if strMessage=="Leaving":  iLevel=int(iLevel)-1
        except:
            raise
