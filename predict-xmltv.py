#import sys
import tester
import ltlib
import xmltvtime

def nextFullHour(datetime):
    tunti=xmltvtime.hour(datetime) + 1
    paiva=xmltvtime.day(datetime) + (1 if tunti>23 else 0)
    return datetime[:6]+str(paiva).zfill(2)+str(tunti%24).zfill(2)+"0000"+datetime[14:]

def removeDuplicates(channel):
    convert={
        "1549.dvb.guide": "mtv3.fi",
        "1501.dvb.guide": "tv1.yle.fi",
        "1502.dvb.guide": "tv2.yle.fi",
        "1503.dvb.guide": "fem.yle.fi"
    }

    if channel in convert:
        return convert[channel]
    else:
        return channel

class XMLTVPredicter(tester.XMLTVHandler):

    currentByChannel={}
    last={}
    current={}
    categories={}
    programs={}
    ohjelmapaikat={}
    rinnakkaisohjelmat={}
    
    def currentProgram(self):
        return self.programs[self.current['title']]
    
    def currentPaikka(self):
        daytime = xmltvtime.dayTime(self.current["start"])
        daytype = xmltvtime.dayType(self.current["start"])
        return removeDuplicates(self.current["channel"])+":"+daytype+":"+str(daytime).zfill(4)
    
    def nearPaikka(self):
        daytime = xmltvtime.dayTime(self.current["start"])
        daytype = xmltvtime.dayType(self.current["start"])
        prefix = removeDuplicates(self.current["channel"]) + ":" + daytype + ":"
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
                if element in self.current:
                    return self.current[element]
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
                currentDuration = self.current["duration"]
                if paikka is not None:
                    assume=self.ohjelmapaikat[paikka]                    
                    if "duration" not in self.programs[assume] or abs(self.programs[assume]["duration"]-currentDuration)<=15:
                        return assume
                if element in self.last:                    
                    if "after" in self.programs[self.last["title"]]:
                        assume = self.programs[self.last["title"]]["after"]
                        if "duration" not in self.programs[assume] or abs(self.programs[assume]["duration"]-currentDuration)<=15:
                            return assume
                if element in self.last:
                    return self.last[element]
            case "sub-title":
                if element+"-"+lang in self.current:
                    return self.current[element+"-"+lang]
                if element+"-"+lang in self.currentProgram():
                    return self.currentProgram()[element+"-"+lang]
            case "categoryn":
                if element in self.current:
                    return self.current[element]
                if element in self.currentProgram():
                    return self.currentProgram()[element]
                if("Uutiset" in self.current['title']):
                    return "20"
                if("Elokuva:" in self.current['title'] or "Subleffa:" in self.current['title']):
                    return "10"                
                if 'sub-title' in self.current and "draama" in self.current['sub-title']:
                    return "10"                                
                if 'sub-title' in self.current and "reality" in self.current['sub-title']:
                    return "30"                                
                if 'sub-title' in self.current and "Kausi" in self.current['sub-title']:
                    return "10"                                
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
                    if removeDuplicates(self.current["channel"]) in ("mtv3.fi","tv1.yle.fi", "tv2.yle.fi"):
                        self.rinnakkaisohjelmat[removeDuplicates(self.current["channel"])+":"+self.current["start"]] = self.current
                self.current={element:content}

            case "start":
                self.current[element]=content
                if removeDuplicates(self.current["channel"]) in ("mtv3.fi","tv1.yle.fi", "tv2.yle.fi"):
                    if removeDuplicates(self.current["channel"])+":"+self.current["start"] in self.rinnakkaisohjelmat:
                        self.current = self.rinnakkaisohjelmat[removeDuplicates(self.current["channel"])+":"+self.current["start"]]

            case "stop":
                self.current[element]=content
                self.current["duration"] = xmltvtime.timeDistance(self.current["start"], content)
                assert self.current["duration"]>=0

            case "title":
                if element not in self.current:
                    self.current[element]=content
                    if content not in self.programs:
                        self.programs[content]={}
                        if ":" in content or " (" in content:
                            uppertitle=content.split(":")[0].split(" (")[0]
                            for key in self.programs:
                                if uppertitle in key:
                                    if "categoryn" in self.programs[key]:
                                        self.programs[content]["categoryn"]=self.programs[key]["categoryn"]
                                    if "sub-title-fi" in self.programs[key]:
                                        self.programs[content]["sub-title-fi"]=self.programs[key]["sub-title-fi"]
                                    if "sub-title-sv" in self.programs[key]:
                                        self.programs[content]["sub-title-sv"]=self.programs[key]["sub-title-sv"]                                        
                                    break
                        self.programs[content]["duration"] = self.current["duration"]
                    self.ohjelmapaikat[self.currentPaikka()] = content
                    if element in self.last:
                        self.programs[self.last["title"]]["after"]=content
                self.currentProgram()[element+"-"+lang] = content

            case "sub-title":
                self.currentProgram()[element+"-"+lang] = content
                self.current[element+"-"+lang]=content

            case "categoryn":
                self.currentProgram()[element] = content
                self.current[element]=content
                if "tv1" in self.current["channel"]:# and not correct:
                    lt.addProgram(self.current["start"], self.current["stop"], self.current["title"], correct)
                    
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