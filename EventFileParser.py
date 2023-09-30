#debug print method
def dprint(text):
    debugging = True
    if debugging : 
        print(text)




#Root node for the tree of microevents
class EventRoot():
    def __init__(self,scan,  identification="", loc=""):
        self.id = identification
        self.location = loc
        self.links = {}
        dprint("Begin parsing tree")
        self.MEroot  = choose_type(scan, self) #microevent root
        
#basic MicroEvent Class
class MicroEvent():
    
    def __init__(self,lima, scan, root):
        if "#\\#" in lima:
            linkk = lima.split("#\\#")
            root.links.update({linkk[0]:self})
            self.line = linkk[1]
        else :
            self.line = lima
        self.scan = scan
        self.root = root
        self.parse()
    def parse(self):
        pass
    def nextMicro(self):
        pass

#extended from MicroEvent
class Dialog(MicroEvent):
    def parse(self):
        #Dialog Syntax
        #dia:who:conditional:emotion:text
        par = self.line.split(":")
        self.type = par[0]
        self.who = par[1]   #blank for narrator
        self.con = par[2]   #determines whether the specific text is displayed
        self.emo = par[3]   #determines which of the sprites will be displayed in the future
        self.text = par[4]
        dprint("Parsed Dialog MicroEvent")
        self.nex = choose_type(self.scan,self.root)
        dprint("Dialog recursion ended successfully!")
    def nextMicro(self):
        return self.nex

#extended from MicroEvent
class Question(MicroEvent):
    def parse(self):
        """Question Syntax
        que:who:conditional:emotion:text
        choice1
        ...
        end
        choice2
        ...
        end"""
        par = self.line.split(":")
        self.type = par[0]
        self.who = par[1]
        self.con = par[2]
        self.emo = par[3]
        self.text = par[4]
        dprint("Parsed Question MicroEvent")
        count = 0
        cho = choose_type(self.scan,self.root)
        self.choices = []
        #answer choice loop
        while cho.type != "end":
            self.choices.append(cho)
            count+=1
            dprint(str(count) + " answer choice successfully loaded!")
            cho = choose_type(self.scan,self.root)
        dprint("Question While Loop Complete!")
    
    def nextMicro(self):
        dprint("not yet implemented")

#extended from MicroEvent
class Choice(MicroEvent):
    def parse(self):
        """Choice Syntax
        cho:who:conditional:text
        ...
        end"""
        par = self.line.split(":")
        self.type = par[0]
        self.who = par[1]
        self.con = par[2]
        self.text = par[3]
        dprint("Parsed choice MicroEvent")
        self.nex = choose_type(self.scan,self.root)
        dprint("choice recursion ended successfully!")

    def nextMicro(self):
        return self.nex

"""
This is intended to be a question where you aren't given options outright.
You place skill cards in a slot and that determines what you do. 
You don't have to write a choice for every possible skill card
Usually one card will be provided that fits
"""
class CardQuestion(MicroEvent):
    def parse(self):
        """Card Question Syntax
        cqu:who:text
        Card1Block
        Card2Block
        ...
        end
        """
        par = self.line.split(":")
        self.type = par[0]
        self.who = par[1]
        self.text = par[2]
        dprint("Parsed Card Question MicroEvent")
        count = 0
        cho = choose_type(self.scan,self.root)
        self.choices = []
        #answer choice loop
        while cho.type != "end":
            self.choices.append(cho)
            count+=1
            dprint(str(count) + " answer card successfully loaded")
            cho = choose_type(self.scan,self.root)
        dprint("Card Question Loop ended successfully")

#this is the card answer choice for Card Questions
#if there is no condition, there is no pass/fail block
class Card(MicroEvent):
    def parse(self):
        #Card Syntax
        #car:card:isProvided:conditional:text
        #...
        #end
        #fail
        #...
        #end
        #end
        par = self.line.split(":")
        self.type = par[0]
        self.card = par[1]
        self.isProvided = par[2]
        self.con = par[3]
        self.text = par[4]
        dprint("Parsed Card Choice MicroEvent")
        self.passed = choose_type(self.scan,self.root)
        dprint("Card Choice Pass Condition Loaded")
        if self.con != "" : 
            self.fail = choose_type(self.scan,self.root)
        dprint("Card Choice recursion exited successfully!")
    def nextMicro(self):
        dprint("not yet implemented")

#fail condition for card choice
class fail(MicroEvent):
    def parse(self):
        #syntax fail:text
        #...
        #end
        par = self.line.split(":")
        self.type = par[0]
        self.text = par[1]
        dprint("Fail con loaded, forehead")
        self.nex = choose_type(self.scan,self.root)
    def nextMicro(self):
        dprint("not yet implemented")




class End(MicroEvent):
    def parse(self):
        self.type = self.line
    def nextMicro(self):
        dprint("If you're reaching this point, it's trying to go past END somehow.")

#Increase a stat or skill level
class increase(MicroEvent):
    def parse(self):
        #syntax
        #inc:isSkill:toIncrease:amount
        par = self.line.split(":")
        self.type = par[0]
        self.isSkill = par[1]
        self.toIncrease = par[2]
        self.amt = par[3]
        dprint("Parsed Skill/Stat Increase")
        self.nex = choose_type(self.scan,self.root)
    def nextMicro(self):
        dprint("not yet implemented")

#Discard a skill card
class discard(MicroEvent):
    def parse(self):
        #syntax
        #dis:skill
        par = self.line.split(":")
        self.type = par[0]
        self.skill = par[1]
        dprint("Parsed discard")
        self.nex = choose_type(self.scan,self.root)
    def nextMicro(self):
        dprint("not yet implemented")

#MicroEvent that sends you back to a link tag
class link(MicroEvent):
    def parse(self):
        par = self.line.split(":")
        self.type = par[0]
        self.nex = self.root.links[par[1]]
        dprint("link to \"" + par[1] + "\" successfully parsed!")  

def choose_type(scan, root) -> MicroEvent :
    line = scan.readline().split("\n")[0]
    linkless = line
    if "#\\#" in line:
        linkless = line.split("#\\#")[1]
    #there's no reason someone would link to end. 
    if (line == "end") : return End(line,scan, root)
    dprint("Read in line: \"" + line + "\"")
    typ = linkless.split(":")[0]
    if (typ == "dia") : return Dialog(line, scan, root)
    if (typ == "que") : return Question(line, scan, root)
    if (typ == "cho") : return Choice(line, scan, root)
    if (typ == "cqu") : return CardQuestion(line, scan, root)
    if (typ == "car") : return Card(line, scan, root)
    if (typ == "fail") : return fail(line, scan, root)
    if (typ == "inc") : return increase(line, scan, root)
    if (typ == "dis") : return discard(line, scan, root)
    if (typ == "lin") : return link(line, scan, root)

class EventFileParser:
    def __init__(self, filename):
        self.file = filename
    #begin recursive parsing process. 
    def parse(self):
        dprint("Opening " + self.file + "...")
        scan = open("test.txt", "r")
        dprint(self.file + " opened successfully!")
        line = scan.readline().split("\n")[0]
        dprint("\""+line+"\" read successfully!")
        #Begin Parsing
        #first line of event file should be formatted as "id:location"
        
        dprint("EventRoot Object Created")
        erinfo = line.split(":")
        evroo = EventRoot(scan, erinfo[0],erinfo[1])
        dprint("EventRoot parsed successfully!")
        
        


