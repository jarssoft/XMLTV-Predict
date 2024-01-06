#!/usr/bin/python3
import xml.sax

class XMLTVHandler(xml.sax.ContentHandler):

    data=0
    element=""

    def startDocument(self):
        pass

    def endDocument(self):
        print("content: "+str(self.data)+" bytes.")
        pass

    def startElement(self, name, attrs):
        self.element=name
        pass

    def endElement(self, name):
        pass

    def ignorableWhitespace(self, whitespace):
        pass
       
    def pureCharacters(self, content):
        prediction=self.predict()
        
        print("element:    '"+self.element+"'")
        print("prediction: '"+str(prediction)+"'")
        print("real:       '"+content+"'")
        
        if(prediction==None):
            self.data+=len(content)
        else:
            if(prediction==content):
                self.data+=0.125
            else:
                self.data+=0.125+len(content)
                
        self.expose(content)

    def characters(self, content):
        content=content.strip().replace("\n","")
        if len(content)>0:
            self.pureCharacters(content)
        
    def skippedEntity(self, name):
        pass

def test(predicter, io):
    parser = xml.sax.make_parser()
    xmltvhandler = predicter
    parser.setContentHandler(xmltvhandler)
    parser.parse(io)