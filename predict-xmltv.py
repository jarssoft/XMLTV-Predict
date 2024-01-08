import sys
import tester

class XMLTVPredicter(tester.XMLTVHandler):

    currentByChannel={}
    last={}
    current={}
    categories={}
    programs={}
    channelchange=True
    ohjelmapaikat={}
    
    def currentProgram(self):
        return self.programs[self.current['title']]
    
    def currentPaikka(self):
        return self.current["channel"]+":"+self.current["start"][8:12]

    def predict(self, element, lang):
        match element:

            case "channel":
                if "channel" in self.last:
                    return self.last['channel']            
            case "start":
                if "stop" in self.last:# and not self.channelchange:
                    return self.last['stop']
            case "stop":
                if "start" in self.current:
                    loppuu=self.current['start']
                    tunti=int(loppuu[8:10]) + 1
                    if tunti<24:
                        return loppuu[:8]+str(tunti).zfill(2)+"0000"+loppuu[14:]

            case "title":
                if "title" in self.current:
                    if "title-"+lang in self.currentProgram():
                        return self.currentProgram()["title-"+lang]
                    else:
                        if lang=="sv":
                            return self.current['title'].replace("(S)","(T)")
                        return self.current['title']
                if self.currentPaikka() in self.ohjelmapaikat:
                    return self.ohjelmapaikat[self.currentPaikka()]
                if "title" in self.last:# and not self.channelchange:
                    return self.last['title']
            case "sub-title":
                if "sub-title-"+lang in self.currentProgram():
                    return self.currentProgram()["sub-title-"+lang]
            case "categoryn":
                if "categoryn" in self.currentProgram():
                    return self.currentProgram()["categoryn"]
                if("Uutiset" in self.current['title']):
                    return "20"       
            case "category":
                if self.current['categoryn'] in self.categories:
                    return self.categories[self.current['categoryn']]
                return 'Movie / Drama'                
            case "value":
                for age in range(0,20):
                    if "("+str(age)+")" in self.current['title']:
                        return str(age)

        return None
    
    def expose(self, element, content, lang):

        if element=="channel":
            #self.channelchange = "channel" not in self.current or self.current["channel"] != content
            if "channel" not in self.current or self.current["channel"] != content:
                if "channel" in self.current:
                    self.currentByChannel[self.current["channel"]]=self.current
                if content in self.currentByChannel:
                    self.last=self.currentByChannel[content]
                else:
                    self.last={}
            else:
                self.last=self.current
            self.current={}

        if element=="title":
            if "title" not in self.current:
                self.current["title"]=content
                if content not in self.programs:
                    self.programs[content]={}
                self.ohjelmapaikat[self.currentPaikka()] = content
            self.currentProgram()["title-"+lang] = content            
        else:
            self.current[element]=content

        if element=="sub-title":
            self.currentProgram()["sub-title-"+lang] = content
        if element=="categoryn":
            self.currentProgram()["categoryn"] = content
        if element=="category":
            self.categories[self.current['categoryn']]=content
    
if(len(sys.argv)<2):
    print ("xmltv-predict.py tvxmlfile")
    exit(0)

tester.test(XMLTVPredicter(), open(sys.argv[1],"r"))