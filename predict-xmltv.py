import sys
import tester

class XMLTVPredicter(tester.XMLTVHandler):

    current={}
    categories={}
    programs={}
    channelchange=True

    def predict(self, element, lang):
        if element=="categoryn":
            if("Uutiset" in self.current['title']):
                return "20"
            if("animaatiosarja" in self.current['sub-title']):
                return "55"            
        if element=="category":
            if self.current['categoryn'] in self.categories:
                return self.categories[self.current['categoryn']]
            return 'Movie / Drama'
        if element=="value":
            for age in range(0,20):
                if "("+str(age)+")" in self.current['title']:
                    return str(age)
        if element=="start":
            if "stop" in self.current and not self.channelchange:
                return self.current['stop']
        if element=="stop":
            if "start" in self.current:
                loppuu=self.current['start']
                tunti=int(loppuu[8:10]) + 1
                if tunti<24:
                    return loppuu[:8]+str(tunti).zfill(2)+"0000"+loppuu[14:]
        if element=="channel" and "channel" in self.current:
            return self.current['channel']

        return None
    
    def expose(self, element, content, lang):
        if element=="channel":
            self.channelchange = "channel" not in self.current or self.current["channel"] != content
        if lang=="" or lang=="fi":
            self.current[element]=content
        if element=="category":      
            self.categories[self.current['categoryn']]=content
    
if(len(sys.argv)<2):
    print ("xmltv-predict.py tvxmlfile")
    exit(0)

tester.test(XMLTVPredicter(), open(sys.argv[1],"r"))

