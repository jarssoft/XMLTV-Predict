#!/usr/bin/python3
import xml.sax
import sys

class XMLTVHandler(xml.sax.ContentHandler):

    data=0

    def startDocument(self):
        pass

    def endDocument(self):
        print("content: "+str(self.data)+" bytes.")
        pass

    def startElement(self, name, attrs):
        pass

    def endElement(self, name):
        pass

    def ignorableWhitespace(self, whitespace):
        pass

    def predict(self):
        return 'Movie / Drama'
        
    def pureCharacters(self, content):
        prediction=self.predict()
        #print("prediction: '"+prediction+"'")
        #print("real:       '"+content+"'")
        if(prediction==None):
            self.data+=len(content)
        else:
            if(prediction==content):
                self.data+=0.125
            else:
                self.data+=0.125+len(content)

    def characters(self, content):
        content=content.strip().replace("\n","")
        if len(content)>0:
            self.pureCharacters(content)
        
    def skippedEntity(self, name):
        pass

if(len(sys.argv)<2):
    print ("xmltv-predict.py tvxmlfile")
    exit(0)

parser = xml.sax.make_parser()
xmltvhandler = XMLTVHandler()
parser.setContentHandler(xmltvhandler)
parser.parse(open(sys.argv[1],"r"))

