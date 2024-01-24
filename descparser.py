import re 

class Desc:

    def __init__(self, desc):
        self._match = re.search("^Kausi ([0-9]+). Jakso ([0-9]+)/([0-9]+).(.*)$", desc)
        if self.hasJakso():
            self._jakso=self._match.group(2)
        else:
            self._desc=desc

    def hasJakso(self):
        return self._match is not None
    
    def isLastJakso(self):
        return self._jakso == self._match.group(3)

    def addJakso(self):
        self._jakso=str(int(self._jakso)+1)

    def str(self):
        if self.hasJakso():
            return "Kausi "+self._match.group(1)+". Jakso "+self._jakso+"/"+self._match.group(3)+"."+self._match.group(4)
        else:
            return self._desc

