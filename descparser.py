import re 

def descParse(desc):
    match = re.search("^(UUSI KAUSI. )?Kausi ([0-9]+). Jakso ([0-9]+)/([0-9]+).(.*)$", desc)
    if match is not None:
        return (int(match.group(3)) + int(match.group(2))*10000, 1, match)
    match = re.search("^(UUSI KAUSI. )?Kausi ([0-9]+). Jakso ([0-9]+)\.(.*)$", desc)
    if match is not None:
        return (int(match.group(3)) + int(match.group(2))*10000, 2, match)
    match = re.search("^Kausi ([0-9]+), ([0-9]+)/([0-9]+)[\. ](.*)$", desc)
    if match is not None:
        return (int(match.group(2)) + int(match.group(1))*10000, 3, match)
    
    #match = re.search("^Kausi ([0-9]+)\. Osa ([0-9]+)(/[0-9]+)?\.$", desc)
    #if match is not None:
    #    return int(match.group(2)) + int(match.group(1))*10000
    
    #match = re.search("Osa ([0-9]+):(.*)$", desc)
    #if match is not None:
    #    return int(match.group(1)) + 1*10000    
    return hash(desc), 0, None

def deschash(desc):
    return descParse(desc)[0]

def changeEpisode(episode, pattern, match):
    return str(match.group(1)) if match.group(1) is not None else "" + "Kausi "+match.group(2)+". Jakso "+str(episode%10000)+"/"+match.group(4)+"."+match.group(5)

def addEpisode(desc, i):
    hash, pattern, match = descParse(desc)    
    
    if pattern==1:
        print(desc)    
        print(i)
        desc = changeEpisode(hash+i, pattern, match)
        print(desc)
    return desc

def nextEpisode(desc):
    return addEpisode(desc, 1)

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

