import re 

def deschash(desc):
    match = re.search("^(UUSI KAUSI. )?Kausi ([0-9]+). Jakso ([0-9]+)/([0-9]+).(.*)$", desc)
    if match is not None:
        return int(match.group(3)) + int(match.group(2))*10000 
    match = re.search("^(UUSI KAUSI. )?Kausi ([0-9]+). Jakso ([0-9]+)\.(.*)$", desc)
    if match is not None:
        return int(match.group(3)) + int(match.group(2))*10000
    match = re.search("^Kausi ([0-9]+), ([0-9]+)/([0-9]+)[\. ](.*)$", desc)
    if match is not None:
        return int(match.group(2)) + int(match.group(1))*10000
    
    #match = re.search("^Kausi ([0-9]+)\. Osa ([0-9]+)(/[0-9]+)?\.$", desc)
    #if match is not None:
    #    return int(match.group(2)) + int(match.group(1))*10000
    
    #match = re.search("Osa ([0-9]+):(.*)$", desc)
    #if match is not None:
    #    return int(match.group(1)) + 1*10000    
    return hash(desc)

class Desc:

    def __init__(self, desc):
        self._match = re.search("^(UUSI KAUSI. )?Kausi ([0-9]+). Jakso ([0-9]+)/([0-9]+).(.*)$", desc)
        if self.hasJakso():
            self._jakso=self._match.group(3)
        else:
            self._desc=desc

    def hasJakso(self):
        return self._match is not None
    
    def __hash__(self):
        if self.hasJakso():
            return int(self._jakso) + int(self._match.group(2))*100
        else:
            return hash(self._desc)
    def isLastJakso(self):
        return self._jakso == self._match.group(4)

    def addJakso(self):
        self._jakso=str(int(self._jakso)+1)

    def str(self):
        if self.hasJakso():
            return str(self._match.group(1))+"Kausi "+self._match.group(2)+". Jakso "+self._jakso+"/"+self._match.group(4)+"."+self._match.group(5)
        else:
            return self._desc

