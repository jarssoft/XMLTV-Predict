import sys
import tester

class XMLTVPredicter(tester.XMLTVHandler):
    def predict(self):
        return 'Movie / Drama'
    
if(len(sys.argv)<2):
    print ("xmltv-predict.py tvxmlfile")
    exit(0)

tester.test(XMLTVPredicter(), open(sys.argv[1],"r"))

