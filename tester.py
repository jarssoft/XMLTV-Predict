#!/usr/bin/python3
import xml.sax

class XMLTVHandler(xml.sax.ContentHandler):

    _data=0
    _datat={}
    _element=""
    _lang=""
    _content=""

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
        if len(self._content)>0:
            self.pureCharacters(self._content, self._element)
        self._content=""
        self._lang=""

    def ignorableWhitespace(self, whitespace):
        pass
       
    #def quest(self, predict):

    def pureCharacters(self, content, element):

        wholeElement=element+" "+self._lang
        #print(wholeElement)
        
        prediction=self.predict(element, self._lang)    

        #print("  prediction: '"+str(prediction)+"'")        
        
        
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
        if(wholeElement not in self._datat):
            self._datat[wholeElement]=0
        self._datat[wholeElement]+=newdata

        self.expose(element, content, self._lang, correct)
        
        #if element=="channel":
        #    print()
        #print((wholeElement+":"+" "*15)[:15]+(str(content)+" "*40)[:40]+" "*10+(str(prediction)[:40] if not correct else "---"))

    def characters(self, content):
        self._content+=content.strip().replace("\n","")

        
    def skippedEntity(self, name):
        pass

def test(predicter, io):
    parser = xml.sax.make_parser()
    xmltvhandler = predicter
    parser.setContentHandler(xmltvhandler)
    parser.parse(io)