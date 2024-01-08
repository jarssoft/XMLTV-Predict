import sys
import tester

def nextFullHour(datetime):
    loppuu=datetime
    tunti=int(loppuu[8:10]) + 1
    paiva=int(loppuu[6:8]) + (1 if tunti>23 else 0)
    return loppuu[:6]+str(paiva).zfill(2)+str(tunti%24).zfill(2)+"0000"+loppuu[14:]
    
class XMLTVPredicter(tester.XMLTVHandler):

    currentByChannel={}
    last={}
    current={}
    categories={}
    programs={}
    ohjelmapaikat={}
    
    def currentProgram(self):
        return self.programs[self.current['title']]
    
    def currentPaikka(self):
        return self.current["channel"]+":"+self.current["start"][8:12]
    
    def nearPaikka(self):
        minute = int(self.current["start"][10:12])
        
        for addminute in [minute+0,  minute+5, minute-5]:
            hour = int(self.current["start"][8:10])
            if addminute>=60:
                hour+=1
            if addminute<0:
                hour-=1
            key = self.current["channel"] + ":" + str(hour).zfill(2) + str(addminute%60).zfill(2)
            if key in self.ohjelmapaikat:
                return key

        return None

    def predict(self, element, lang):
        match element:

            case "channel":
                if "channel" in self.last:
                    return self.last['channel']            
            case "start":
                if "stop" in self.last:
                    return self.last['stop']
            case "stop":
                if "start" in self.current:
                    return nextFullHour(self.current['start'])

            case "title":
                if "title" in self.current:
                    if "title-"+lang in self.currentProgram():
                        return self.currentProgram()["title-"+lang]
                    else:
                        if lang=="sv":
                            return self.current['title'].replace("(S)","(T)")
                        return self.current['title']
                paikka = self.nearPaikka()
                if paikka is not None:
                    return self.ohjelmapaikat[paikka]
                if "title" in self.last:
                    return self.last['title']
            case "sub-title":
                if "sub-title-"+lang in self.currentProgram():
                    return self.currentProgram()["sub-title-"+lang]
            case "categoryn":
                if "categoryn" in self.currentProgram():
                    return self.currentProgram()["categoryn"]
                if("Uutiset" in self.current['title']):
                    return "20"
                if "categoryn" in self.last:
                    return self.last['categoryn']
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