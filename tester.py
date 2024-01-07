#!/usr/bin/python3
import xml.sax

class XMLTVHandler(xml.sax.ContentHandler):

    _data=0
    _element=""
    _lang=""

    def startDocument(self):
        pass

    def endDocument(self):
        print("content: "+str(self._data)+" bytes.")        
        pass

    def startElement(self, name, attrs):
        self._element=name
        if "lang" in attrs :
            #print(attrs["lang"])
            self._lang=attrs["lang"]
        if name=="programme":
            self.pureCharacters(attrs["channel"], "channel")
            self.pureCharacters(attrs["start"], "start")
            self.pureCharacters(attrs["stop"], "stop")            

    def endElement(self, name):
        self._lang=""
        pass

    def ignorableWhitespace(self, whitespace):
        pass
       
    def pureCharacters(self, content, element):
        prediction=self.predict(element, self._lang)
        
        print("element:    '"+element+"'")
        print("prediction: '"+str(prediction)+"'")
        print("real:       '"+content+"'")
        
        if(prediction==None):
            self._data+=len(content)
        else:
            if(prediction==content):
                self._data+=0.125
            else:
                self._data+=0.125+len(content)

        self.expose(element, content, self._lang)

    def characters(self, content):
        content=content.strip().replace("\n","")
        if len(content)>0:
            self.pureCharacters(content, self._element)
        
    def skippedEntity(self, name):
        pass

def test(predicter, io):
    parser = xml.sax.make_parser()
    xmltvhandler = predicter
    parser.setContentHandler(xmltvhandler)
    parser.parse(io)