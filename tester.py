#!/usr/bin/python3
import xml.sax

class XMLTVHandler(xml.sax.ContentHandler):

    _compressed={}
    _original={}
    _element=""
    _lang=""
    _content=""
    _verbosemode=False

    def startDocument(self):
        pass

    def endDocument(self):
        print("--------------------------------------------------")
        print("element         compressed   original        ratio")
        print("--------------------------------------------------")
        totalcompressed=0
        totaloriginal=0        
        for key in self._compressed.keys():
            totalcompressed += self._compressed[key]
            totaloriginal += self._original[key]
            print((key+" "*15)[:15],(" "*20+str(int(self._compressed[key])))[-10:], (" "*20+str(self._original[key]))[-10:], (" "*20+str(int(self._compressed[key]/self._original[key]*100)))[-10:],"%")
        print("--------------------------------------------------")
        #print("content: "+str(self._data)+" bytes.")
        print(("total"+" "*15)[:15],(" "*20+str(int(totalcompressed)))[-10:], (" "*20+str(totaloriginal))[-10:], (" "*20+str(int(totalcompressed/totaloriginal*100)))[-10:],"%")
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

        if(wholeElement not in self._compressed):
            self._compressed[wholeElement]=0
            self._original[wholeElement]=0                    
        
        correct=False
        if(prediction==None):
            newdata=len(content)
        else:
            if(prediction==content):
                newdata=0.125
                correct=True                
            else:
                newdata=0.125+len(content)

        self._compressed[wholeElement]+=newdata
        self._original[wholeElement]+=len(content)
        
        self.expose(element, content, self._lang, correct)
        
        if self._verbosemode:
            if element=="channel":
                print()
            print((wholeElement+":"+" "*15)[:15]+(str(content)+" "*40)[:40]+" "*10+(str(prediction)[:40] if not correct else "---"))

    def characters(self, content):
        self._content+=content.strip().replace("\n","")

        
    def skippedEntity(self, name):
        pass

    def setVerbose(self, verbosemode):
        self._verbosemode=verbosemode

def test(predicter, io):
    parser = xml.sax.make_parser()
    xmltvhandler = predicter
    parser.setContentHandler(xmltvhandler)
    parser.parse(io)