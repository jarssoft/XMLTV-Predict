#import sys
import tester
import ltlib
import xmltvtime

def nextFullHour(datetime):
    tunti=xmltvtime.hour(datetime) + 1
    paiva=xmltvtime.day(datetime) + (1 if tunti>23 else 0)
    return datetime[:6]+str(paiva).zfill(2)+str(tunti%24).zfill(2)+"0000"+datetime[14:]
    
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
        daytime = xmltvtime.dayTime(self.current["start"])
        daytype = xmltvtime.dayType(self.current["start"])
        return self.current["channel"]+":"+daytype+":"+str(daytime).zfill(4)
    
    def nearPaikka(self):
        daytime = xmltvtime.dayTime(self.current["start"])
        daytype = xmltvtime.dayType(self.current["start"])
        prefix = self.current["channel"] + ":" + daytype + ":"
        for addminute in (0, 5, -5):            
            key = prefix + str(daytime+addminute).zfill(4)
            if key in self.ohjelmapaikat:
                return key
        return None

    def predict(self, element, lang):
        match element:

            case "channel":
                if element in self.last:
                    return self.last[element]            
            case "start":
                if "stop" in self.last:
                    return self.last['stop']
            case "stop":
                start = self.current['start']
                paikka = self.nearPaikka()
                assume=None
                if paikka is not None:
                    assume = self.ohjelmapaikat[paikka]                
                if element in self.last:
                    if "after" in self.programs[self.last["title"]]:
                        assume = self.programs[self.last["title"]]["after"]                
                if assume is not None:
                    if assume in self.programs and "duration" in self.programs[assume]:
                        return xmltvtime.addMinuts(start, self.programs[assume]["duration"])
                return nextFullHour(start)
            case "title":
                if element in self.current:
                    if element+"-"+lang in self.currentProgram():
                        return self.currentProgram()[element+"-"+lang]
                    else:
                        if lang=="sv":
                            return self.current[element].replace("(S)","(T)")
                        return self.current[element]
                paikka = self.nearPaikka()
                if paikka is not None:
                    return self.ohjelmapaikat[paikka]
                if element in self.last:                    
                    if "after" in self.programs[self.last["title"]]:
                        return self.programs[self.last["title"]]["after"]
                if element in self.last:
                    return self.last[element]
            case "sub-title":
                if element+"-"+lang in self.currentProgram():
                    return self.currentProgram()[element+"-"+lang]
            case "categoryn":
                if element in self.currentProgram():
                    return self.currentProgram()[element]
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
    
    def expose(self, element, content, lang, correct):

        match element:
            case "channel":
                if element not in self.current or self.current[element] != content:
                    if element in self.current:
                        self.currentByChannel[self.current[element]]=self.current
                    if content in self.currentByChannel:
                        self.last=self.currentByChannel[content]
                    else:
                        self.last={}
                else:
                    self.last=self.current
                self.current={element:content}

            case w if w in ["start", "stop"]:
                self.current[element]=content            
        
            case "title":
                if element not in self.current:
                    self.current[element]=content
                    if content not in self.programs:
                        self.programs[content]={}
                        duration = xmltvtime.timeDistance(self.current["start"], self.current["stop"]) 
                        if duration>0:
                            self.programs[content]["duration"] =duration
                    #if xmltvtime.day(self.current["start"]) not in (19, 20, 25, 26, 27): #Ei viikonloppua
                    self.ohjelmapaikat[self.currentPaikka()] = content
                    if element in self.last:
                        self.programs[self.last["title"]]["after"]=content
                    if "tv1" in self.current["channel"]:# and not correct:
                        lt.addProgram(self.current["start"], self.current["stop"], content, "Yle Uutis" in content)
                self.currentProgram()[element+"-"+lang] = content

            case "sub-title":
                self.currentProgram()[element+"-"+lang] = content
            case "categoryn":
                self.currentProgram()[element] = content
                self.current[element]=content
            case "category":
                self.categories[self.current['categoryn']]=content
    
#if(len(sys.argv)<2):
#    print ("xmltv-predict.py tvxmlfile")
#    exit(0)

lt = ltlib.LongTerm("out.svg")
predicter = XMLTVPredicter()
#file=sys.argv[1]
file="/home/jari/media/lataukset/tvtiivis/ohjelmat-yle-2.xml"
tester.test(predicter, open(file,"r"))
#print(predicter.ohjelmapaikat)
lt.save()