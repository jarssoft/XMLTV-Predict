import sys
import tester

class XMLTVPredicter(tester.XMLTVHandler):

    current={}
    categories={}
    programs={}
    channelchange=True

    def currentProgramName(self):
        return self.current['title']
    
    def currentProgram(self):
        return self.programs[self.current['title']]

    def predict(self, element, lang):
        match element:

            case "channel":
                if "channel" in self.current:
                    return self.current['channel']            
            case "start":
                if "stop" in self.current and not self.channelchange:
                    return self.current['stop']
            case "stop":
                if "start" in self.current:
                    loppuu=self.current['start']
                    tunti=int(loppuu[8:10]) + 1
                    if tunti<24:
                        return loppuu[:8]+str(tunti).zfill(2)+"0000"+loppuu[14:]

            case "title":
                if lang!="fi":
                    if "title-"+lang in self.currentProgram():
                        return self.currentProgram()["title-"+lang]
                    else:
                        return self.current['title']
            case "sub-title":
                if "sub-title-"+lang in self.currentProgram():
                    return self.currentProgram()["sub-title-"+lang]
            case "categoryn":
                if("Uutiset" in self.current['title']):
                    return "20"
                if("animaatiosarja" in self.current['sub-title']):
                    return "55"            
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
            self.channelchange = "channel" not in self.current or self.current["channel"] != content
        if lang=="" or lang=="fi":
            self.current[element]=content
            if element=="title":
                if self.currentProgramName() not in self.programs:
                    self.programs[self.currentProgramName()]={}
        else:
            if element=="title":
                    self.currentProgram()["title-"+lang] = content
        if element=="sub-title":
                self.currentProgram()["sub-title-"+lang] = content
        if element=="category":
            self.categories[self.current['categoryn']]=content
    
if(len(sys.argv)<2):
    print ("xmltv-predict.py tvxmlfile")
    exit(0)

tester.test(XMLTVPredicter(), open(sys.argv[1],"r"))