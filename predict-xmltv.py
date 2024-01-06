import sys
import tester

class XMLTVPredicter(tester.XMLTVHandler):

    current={}

    categories={
        '10':'Movie / Drama',
        '17':'Movie - serious/classical/religious/historical movie/drama',
        '20':'News / Current Affairs',
        '31':'Show - game show/quiz/contest',
        '30':'Show / Game Show',
        '40':'Sports',
        '45':'Sports - team sports (excluding football)',
        '50':'Childrens / Youth',
        '51':'Children - pre-school children\'s programmes',
        '55':'Children - cartoons/puppets',
        '60':'Music / Ballet / Dance',
        '73':'Arts - religion',
        '81':'Social - magazines/reports/documentary',
        '91':'Education - nature/animals/environment',
        'a0':'Leisure / Hobbies',
    }

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
    
if(len(sys.argv)<2):
    print ("xmltv-predict.py tvxmlfile")
    exit(0)

tester.test(XMLTVPredicter(), open(sys.argv[1],"r"))

