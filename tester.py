#!/usr/bin/python3
import xml.sax

class XMLTVHandler(xml.sax.ContentHandler):

    _data=0
    _datat={}
    _element=""
    _lang=""

    def startDocument(self):
        pass

    def endDocument(self):
        print("content: "+str(self._datat)+" bytes.")        
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
       
    #def quest(self, predict):

    def pureCharacters(self, content, element):

        print(element+" "+self._lang)
        
        prediction=self.predict(element, self._lang)    

        print("  prediction: '"+str(prediction)+"'")        
        
        correct=False
        if(prediction==None):
            newdata=len(content)
        else:
            if(prediction==content):
                newdata=0.125
                correct=True
            else:
                newdata=0.125+len(content)

        self._data+=newdata
        if(element not in self._datat):
            self._datat[element]=0
        self._datat[element]+=newdata

        self.expose(element, content, self._lang, correct)
        print("  real:       '"+content+"'")

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