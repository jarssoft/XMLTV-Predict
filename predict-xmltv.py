import sys
import tester

def minute(time):
    return int(time[10:12])

def hour(time):
    return int(time[8:10])

def nextFullHour(datetime):
    loppuu=datetime
    tunti=hour(loppuu) + 1
    paiva=int(loppuu[6:8]) + (1 if tunti>23 else 0)
    return loppuu[:6]+str(paiva).zfill(2)+str(tunti%24).zfill(2)+"0000"+loppuu[14:]

def timeDistance(start, stop):
    return (hour(stop) - hour(start)) * 60 + (minute(stop) - minute(start))

def addMinuts(time, delta):
    minuts = hour(time) * 60 + minute(time) + delta
    return time[:8] + str(int(minuts/60)).zfill(2) + str(minuts%60).zfill(2) + time[12:]

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
        
        for addminute in [minute,  minute+5, minute-5]:
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
                        return addMinuts(start, self.programs[assume]["duration"])
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
    
    def expose(self, element, content, lang):

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
                        self.programs[content]["duration"] = timeDistance(self.current["start"], self.current["stop"]) 
                    self.ohjelmapaikat[self.currentPaikka()] = content
                    if element in self.last:
                        self.programs[self.last["title"]]["after"]=content
                self.currentProgram()[element+"-"+lang] = content

            case "sub-title":
                self.currentProgram()[element+"-"+lang] = content
            case "categoryn":
                self.currentProgram()[element] = content
                self.current[element]=content
            case "category":
                self.categories[self.current['categoryn']]=content
    
if(len(sys.argv)<2):
    print ("xmltv-predict.py tvxmlfile")
    exit(0)

predicter = XMLTVPredicter()
tester.test(predicter, open(sys.argv[1],"r"))
#print(predicter.ohjelmapaikat)