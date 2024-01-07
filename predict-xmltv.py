import sys
import tester

class XMLTVPredicter(tester.XMLTVHandler):

    current={}
    categories={}
    channelchange=True

    def predict(self, element):
        if element=="category":
            if self.current['categoryn'] in self.categories:
                return self.categories[self.current['categoryn']]
            if("Uutiset" in self.current['title']):
                return 'News / Current Affairs'
            else:
                return 'Movie / Drama'
        if element=="value":
            for age in range(0,20):
                if "("+str(age)+")" in self.current['title']:
                    return str(age)
        if element=="start":
            if "stop" in self.current and not self.channelchange:
                return self.current['stop']
        if element=="channel" and "channel" in self.current:
            return self.current['channel']

        
        return None
    
    def expose(self, element, content):
        if element=="channel":
            self.channelchange = "channel" not in self.current or self.current["channel"] != content
        self.current[element]=content
        if element=="category":      
            self.categories[self.current['categoryn']]=content
    
if(len(sys.argv)<2):
    print ("xmltv-predict.py tvxmlfile")
    exit(0)

tester.test(XMLTVPredicter(), open(sys.argv[1],"r"))

