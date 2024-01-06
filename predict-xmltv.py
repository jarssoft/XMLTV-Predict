import sys
import tester
import genre

class XMLTVPredicter(tester.XMLTVHandler):

    current={}
    categories={}

    def predict(self):
        if self.element=="category":
            if self.current['categoryn'] in self.categories:
                return self.categories[self.current['categoryn']]
            if("Uutiset" in self.current['title']):
                return 'News / Current Affairs'
            else:
                return 'Movie / Drama'
        if self.element=="value":
            for age in range(0,20):
                if "("+str(age)+")" in self.current['title']:
                    return str(age)
        else: 
            return None
    
    def expose(self, content):
        self.current[self.element]=content
        if self.element=="category":      
            self.categories[self.current['categoryn']]=content
    
if(len(sys.argv)<2):
    print ("xmltv-predict.py tvxmlfile")
    exit(0)

tester.test(XMLTVPredicter(), open(sys.argv[1],"r"))

