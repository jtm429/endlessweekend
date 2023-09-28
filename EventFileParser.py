#debug print method
def dprint(text):
    debugging = true
    if debugging print(text)


#Root node for the tree of microevents
class EventRoot:
    def __init__(self):
        self.id
        self.location
        self.MEroot  #microevent root
    def parseMicro(self, scan):
        
#basic MicroEvent Class
class MicroEvent():
    
    def __init__(self,lima, scan):
        self.line = lima
        self.scan = scan
        parse()
    def parse(self):
        pass
    def nextMicro(self):
        pass

#extended from MicroEvent
class Dialog(MicroEvent):
    def parse(self):
        #Dialog Syntax
        #dia:who:condition:emotion:text
        par = self.line.split(":")
        self.type = par[0]
        self.who = par[1]
        self.con = par[2]
        self.emo = par[3]
        self.text = par[4]
        dprint("Parsed Dialog MicroEvent")
        self.nex = choose_type(self.scan)
        dprint("Dialog recursion ended successfully!")
    def nextMicro(self):
        return self.nex

class Question(MicroEvent):
    def parse(self):
        """Question Syntax
        que:who:conditional:emotion:text"""

def choose_type(scan) -> MicroEvent :
    line = scan.readLine()
    typ = line.split(":")[0]
    if (typ == "dia") return Dialog(line, scan)

class EventFileParser:
    def __init__(self, filename):
        self.file = filename
    #begin recursive parsing process. 
    def parse(self):
        dprint("Opening " + self.file + "..."
        scan = open("test.txt", "r")
        dprint(self.file + " opened successfully!")
        line = scan.readLine()
        dprint("\""+line+"\" read successfully!")
        #Begin Parsing
        #first line of event file should be formatted as "id:location"
        evroo = EventRoot()
        dprint("EventRoot Object Created")
        erinfo = line.split(":")
        evroo.id = erinfo[0]
        evroo.location = erinfo[1]
        dprint("EventRoot parsed successfully!")
        dprint("Begin parsing tree")
        evroo.MEroot = 
        


