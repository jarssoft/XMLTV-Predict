import sys
import tester

class XMLTVPredicter(tester.XMLTVHandler):

    current={}
    categories={}

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
        else: 
            return None
    
    def expose(self, element, content):
        self.current[element]=content
        if element=="category":      
            self.categories[self.current['categoryn']]=content
    
if(len(sys.argv)<2):
    print ("xmltv-predict.py tvxmlfile")
    exit(0)

tester.test(XMLTVPredicter(), open(sys.argv[1],"r"))

