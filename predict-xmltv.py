import sys
import tester
import ltlib
import xmltvtime
import descparser

nelonenMedia = ("nelonen.fi", "liv.nelonen.fi", "jim.nelonen.fi")
disney = ("1525.dvb.guide", "1522.dvb.guide", "1518.dvb.guide", "1585.dvb.guide")

class XMLTVPredicter(tester.XMLTVHandler):

    currentByChannel={}
    last={}
    current={}
    categories={}
    programs={}
    ohjelmapaikat={}
    rinnakkaisohjelmat={}
    stops={}
    
    def currentProgram(self):
        return self.programs[self.current['title']]
    
    def dayProfileName(self):
        daytype = xmltvtime.dayType(self.current["start"])
        return self.uniqueChannel() + ":" + daytype
    
    def currentPaikka(self):
        prefix = self.dayProfileName()
        daytime = xmltvtime.dayTime(self.current["start"])
        return prefix + ":" + str(daytime).zfill(4)
    
    def nearPaikka(self):
        prefix = self.dayProfileName()
        daytime = xmltvtime.dayTime(self.current["start"])
        for addminute in (0, 5, -5):
            key = prefix + ":" + str(daytime+addminute).zfill(4)
            if key in self.ohjelmapaikat:
                return self.ohjelmapaikat[key]
        return None

    def ageMatch(self, current, episode):
        return "age" not in current or "age" in episode and current["age"] == episode["age"]
    
    def durationConflict(self, program):
        return "duration" in program and abs(program["duration"]-self.current["duration"]) > 15

    duplicates={
        "1549.dvb.guide": "mtv3.fi",
        "1501.dvb.guide": "tv1.yle.fi",
        "1502.dvb.guide": "tv2.yle.fi",
        "1503.dvb.guide": "fem.yle.fi"
    }

    def uniqueChannel(self):
        if self.current["channel"] in self.duplicates:
            return self.duplicates[self.current["channel"]]
        else:
            return self.current["channel"]
    
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
            #if "mtv3.fi" in self.current["channel"]:
            #    return xmltvtime.nextFullHour(start)    

            programname = None
            
            # arvataan ohjelma peräkkäisyyden perusteella
            if element in self.last:
                if "after" in self.programs[self.last["title"]]:
                    programname = self.programs[self.last["title"]]["after"]
                else:
                    programname = self.last["title"]

            # samaan aikaan tulevat ohjelmat        
            if self.nearPaikka() is not None:
                programname = self.nearPaikka()

            # etsitään ohjelmaa seuraava aika, jolloin on paljon loppuvia ohjelmia
            thisStart = xmltvtime.totalTime(self.current["start"])
            bestduration=(0, 0)            
            if self.current["channel"] in self.stops:
                for duration in range(5, 65, 5):
                    sametimestops=0
                    for stop in self.stops[self.current["channel"]]:
                        if (stop-(thisStart+duration)) % (24*60) == 0:
                            if abs(stop - (thisStart+duration)) <= (24*60):
                                sametimestops+=2
                            else:
                                sametimestops+=1
                    if sametimestops > bestduration[1]:
                        bestduration = (duration, sametimestops)
                    if bestduration[1]>2:
                        return xmltvtime.addMinuts(start, bestduration[0])

            if programname is not None:
                if "duration" in self.programs[programname]:
                    return xmltvtime.addMinuts(start, self.programs[programname]["duration"])
            return xmltvtime.nextFullHour(start)
        
        case "title":
            if element in self.current:
                if element+"-"+lang in self.currentProgram():
                    return self.currentProgram()[element+"-"+lang]
                else:
                    if lang=="sv":
                        if element+"-no" in self.currentProgram():
                            return self.currentProgram()[element+"-no"]
                        return self.current[element].replace("(S)","(T)")
                    if lang=="no":
                        if element+"-da" in self.currentProgram():
                            return self.currentProgram()[element+"-da"]
                    return self.current[element]
            programname = self.nearPaikka()
            if programname is not None:              
                if not self.durationConflict(self.programs[programname]):
                    return programname
            if element in self.last:                    
                if "after" in self.programs[self.last["title"]]:
                    programname = self.programs[self.last["title"]]["after"]
                    if not self.durationConflict(self.programs[programname]):
                        return programname
                    
            if element in self.last:
                return self.last[element]
            
        case "sub-title": 
            if element+"-"+lang in self.current:
                return self.current[element+"-"+lang]
            
            if "episodes" in self.currentProgram():

                episodehash = None               
                programEpisodes = self.currentProgram()["episodes"]

                if "episode" in self.current:
                    episodehash = self.current["episode"]
                else:
                    thisStart = xmltvtime.totalTime(self.current["start"])
                    episodeAdd = None
                    episodeform = ""

                    # Viimeksi mainitun ohjelman episodi
                    if "last-episode" in self.currentProgram():                        
                        episodehash=self.currentProgram()["last-episode"]
                        if(episodehash+1 in programEpisodes):
                            if self.ageMatch(self.current, programEpisodes[episodehash+1]):
                                episodehash+=1

                    # Jos samanniminen ohjelma tulee samaan aikaan päivästä, 
                    # jaksoero on yhtäkuin päiväero
                    for episodeKey, episodeValue in programEpisodes.items():
                        episodeStart = xmltvtime.totalTime(episodeValue["start"])
                        if ((episodeStart-thisStart) % (60*24)) == 0:
                            jakso = int((thisStart-episodeStart) / (60*24))
                            if episodeKey+jakso in programEpisodes.keys():
                                episodehash = episodeKey + jakso
                            elif self.current["channel"] in nelonenMedia+disney:
                                if "fi" in programEpisodes[episodeKey]:
                                    episodeform=programEpisodes[episodeKey]["fi"]
                                    episodeAdd=jakso
                                    
                    # Ohjelmilla on usein tietty "uusinta-intervalli"
                    if "reruns" in self.currentProgram():                        
                        for episodeKey, episodeValue in programEpisodes.items():
                            episodeStart = xmltvtime.totalTime(episodeValue["start"])
                            if abs(episodeStart - thisStart) in self.currentProgram()["reruns"]:
                                if self.ageMatch(self.current, programEpisodes[episodeKey]):
                                    episodehash=episodeKey
                                    break
        
                    # Samannimiset peräkkäiset ohjelmat ovat usein myös peräkkäisiä episodeja
                    if "title" in self.last and self.last["title"] == self.current["title"]:
                        if "episode" in self.last:
                            last = self.last["episode"]
                            nextepisode=last+1
                            if nextepisode in programEpisodes:                                
                                if self.ageMatch(self.current, programEpisodes[nextepisode]):
                                    episodehash=nextepisode
                            elif self.current["channel"] in nelonenMedia+disney:
                                if "fi" in programEpisodes[last]:
                                    episodeform=programEpisodes[last]["fi"]
                                    episodeAdd=1

                    if episodeAdd is not None:
                        return descparser.addEpisode(episodeform, episodeAdd)

                if episodehash is not None:
                    if lang in programEpisodes[episodehash]:
                        return programEpisodes[episodehash][lang]       

            if lang=="sv":
                if element+"-no" in self.current:
                    text=self.current[element+"-no"]
                    text=text.replace("fra", "från")
                    text=text.replace("familieserie", "familjeserie")
                    text=text.replace("komiserie", "komediserie")
                    text=text.replace("underhollning", "underhållning")
                    return text
                if element+"-fi" in self.current:
                    text=self.current[element+"-fi"]
                    text=text.replace("Magasin", "Makasiini")
                    return text
            if lang=="no":
                if element+"-da" in self.current:
                    text=self.current[element+"-da"]
                    text=text.replace("komedieserie", "komiserie")
                    text=text.replace("animationsserie", "animasjonsserie")
                    return text                        
                
        case "categoryn":
            if element in self.current:
                return self.current[element]
            if element in self.currentProgram():
                return self.currentProgram()[element]
            if("Uutiset" in self.current['title']):
                return "20"
            if("Elokuva:" in self.current['title'] or "Subleffa:" in self.current['title']):
                return "10"
            if(self.current['duration'] > 70 and self.current['duration'] < 200):
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
            if "age" in self.current:
                for age in (7, 11, 12, 15, 16, 18):
                    if " ("+str(age)+")" == self.current["age"]:
                        return str(age)
    
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
                if self.uniqueChannel() in self.duplicates.values():
                    key = self.uniqueChannel()+":"+self.current["start"]
                    self.rinnakkaisohjelmat[key] = self.current
            self.current={element:content}

        case "start":
            self.current[element]=content
            if self.uniqueChannel() in self.duplicates.values():
                key = self.uniqueChannel()+":"+self.current["start"]
                if key in self.rinnakkaisohjelmat:
                    self.current = self.rinnakkaisohjelmat[key]

        case "stop":
            self.current[element] = content
            self.current["duration"] = xmltvtime.timeDistance(self.current["start"], content)
            assert self.current["duration"] >= 0
            
            if self.current["channel"] not in self.stops:
                self.stops[self.current["channel"]] = []
            self.stops[self.current["channel"]].append(xmltvtime.totalTime(content))

            if "mtv3.fi" in self.current["channel"]:
                # and "Violetta" in self.current["title"]:
                lt.setInterval(self.current["start"], self.current["stop"])
                lt.addProgram(self.current["start"][-12:-8], correct)

        case "title":
            if " (" in content:
                self.current["age"] = " (" + content.split(" (")[-1]

            if element not in self.current:
                self.current[element]=content
                if content not in self.programs:
                    self.programs[content]={"duration": self.current["duration"]}
                self.ohjelmapaikat[self.currentPaikka()] = content
                if element in self.last:
                    self.programs[self.last[element]]["after"]=content
            self.currentProgram()[element+"-"+lang] = content
            if "age" in self.current:
                self.currentProgram()["age"] = self.current["age"]

        case "sub-title":                
            if "episode" not in self.current:
                episodehash=descparser.deschash(content)
                if "episodes" not in self.currentProgram():
                    self.currentProgram()["episodes"]={}
                if episodehash not in self.currentProgram()["episodes"]:
                    self.currentProgram()["episodes"][episodehash]={}
                else:
                    thisStart=xmltvtime.totalTime(self.current["start"])
                    lastShow=self.currentProgram()["episodes"][episodehash]
                    lastStart=xmltvtime.totalTime(lastShow["start"])
                    rerunInterval = abs(thisStart - lastStart)                        
                    if(rerunInterval>60):
                        if "reruns" not in self.currentProgram():
                            self.currentProgram()["reruns"]=[]
                        if rerunInterval not in self.currentProgram()["reruns"]:
                            self.currentProgram()["reruns"].append(rerunInterval)
                self.currentProgram()["episodes"][episodehash]["start"] = self.current["start"]
                if "age" in self.current:
                    self.currentProgram()["episodes"][episodehash]["age"] = self.current["age"]

                self.current["episode"]=episodehash
            self.currentProgram()["episodes"][self.current["episode"]][lang] = content  
            self.currentProgram()["last-episode"] = self.current["episode"]
            self.current[element+"-"+lang]=content

            #if "fox" in self.current["channel"] and "Simpsonit" in self.current["title"]:
            #if "sub.fi" in self.current["channel"] and "Salatut" in self.current["title"]:


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
predicter.setVerbose("-v" in sys.argv)

#file=sys.argv[1]
file="/home/jari/media/lataukset/tvtiivis/ohjelmat-yle-2.xml"
tester.test(predicter, open(file,"r"))
#print(predicter.programs)
lt.save()