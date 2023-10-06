#debug print method
def dprint(text, debug=False):
    
    if debug : 
        print("debug:"+text)




#Root node for the tree of microevents
class EventRoot():
    def __init__(self,scan,  identification="", loc=""):
        self.id = identification
        self.location = loc
        self.links = {}
        dprint("Begin parsing tree")
        self.MEroot  = choose_type(scan, self) #microevent root
    def encode(self, filename):
        data = self.id + ":" + self.location +"\n"
        data += self.MEroot.encode()
        data += "end:file"
        file = open(filename, "w")
        file.write(data)
        file.close()


        
#basic MicroEvent Class
class MicroEvent():
    
    def __init__(self,lima, scan, root):
        self.link=""
        if "#\\#" in lima:
            linkk = lima.split("#\\#")
            root.links.update({linkk[0]:self})
            self.line = linkk[1]
            self.link = linkk[0]+"#\\#"
        else :
            self.line = lima
            
        self.scan = scan
        self.root = root
        self.parse()
    def parse(self):
        pass
    def encode(self)-> str:
        pass
    def __str__(self):
        return self.encode()

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
    def encode(self):
        line = self.link+self.type + ":"+self.who + ":"+ self.con + ":"+ self.emo + ":"+ self.text +"\n"
        dprint(line)
        line += self.nex.encode()
        return line

#extended from MicroEvent
class Question(MicroEvent):
    def parse(self):
        """Question Syntax
        que:who:conditional:emotion:text
        choice1
        ...
        end:cho
        choice2
        ...
        end:cho
        end:que
        
        """
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
        #for question to be conditional you need to have a fail state
        self.nex = ""
        if(self.con != ""):
            dprint("Conditional question fail state")
            self.nex = choose_type(self.scan, self.root)
        dprint("Question While Loop Complete!")
    def encode(self):
        line = self.link +self.type + ":"+self.who + ":"+ self.con + ":"+ self.emo + ":"+ self.text +"\n"
        dprint(line)
        for choice in self.choices:
            line += choice.encode()
        line += "end:que\n"
        #if it has nex it calls encode
        #as per the __str__ defined in 
        #MicroEvent otherwise its ""
        line += str(self.nex)
        return line
    

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
    def encode(self):
        line = self.link+self.type + ":"+self.who + ":"+ self.con + ":"+ self.text +"\n"
        dprint(line)
        line += self.nex.encode()
        line += "end:cho\n"
        return line


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
        self.choices = {}
        #answer choice loop
        while cho.type != "end":
            dprint(cho.card+ " " +str(cho))
            self.choices.update({cho.card :cho})
            count+=1
            dprint(str(count) + " answer card successfully loaded")
            cho = choose_type(self.scan,self.root)
        dprint("Card Question Loop ended successfully")
    def encode(self):
        line = self.link +self.type + ":"+self.who + ":"+ self.text +"\n"
        dprint(line)
        for key, event in self.choices.items():
            line += event.encode()
        line += "end:cqu\n"
        return line

#this is the card answer choice for Card Questions
#if there is no condition, there is no pass/fail block
class Card(MicroEvent):
    def parse(self):
        #Card Syntax
        #car:card:isProvided:conditional:text
        #...
        #end:pass
        #fail
        #...
        #end:fail
        par = self.line.split(":")
        self.type = par[0]
        self.card = par[1]
        self.isProvided = par[2]
        self.con = par[3]
        self.text = par[4]
        dprint("Parsed Card Choice MicroEvent")
        self.passed = choose_type(self.scan,self.root)
        dprint("Card Choice Pass Condition Loaded")
        self.fail = ""
        if self.con != "" : 
            self.fail = choose_type(self.scan,self.root)
        dprint("Card Choice recursion exited successfully!")
    def encode(self):
        line = self.link+self.type + ":"+self.card + ":"+str(int(self.isProvided)) + ":" + self.con + ":"+ self.text +"\n"
        dprint(line)
        line += self.passed.encode()
        line += "end:pass\n"
        line +=str(self.fail)
        return line

#fail condition for card choice
class Fail(MicroEvent):
    def parse(self):
        #syntax fail:text
        #...
        #end:fail
        par = self.line.split(":")
        self.type = par[0]
        self.text = par[1]
        dprint("Fail con loaded, forehead")
        self.nex = choose_type(self.scan,self.root)
    def encode(self) -> str:
        line = self.link + self.type + ":" + self.text + "\n"
        dprint(line)
        line+= self.nex.encode()
        line+= "end:fail\n"
        return line




class End(MicroEvent):
    def parse(self):
        if ":" in self.line:
            par = self.line.split(":")
            self.type = par[0]
            self.end = par[1]
        else : self.type = self.line
    def encode(self) -> str:
        dprint("end encode")
        return "" #Ends are needed within the tree, but they're managed by the MicroEvent they're ending

#Increase a stat or skill level
class Increase(MicroEvent):
    def parse(self):
        #syntax
        #inc:isSkill:toIncrease:amount
        par = self.line.split(":")
        self.type = par[0]
        self.isSkill = par[1]
        self.toIncrease = par[2]
        self.amt = int(par[3])
        dprint("Parsed Skill/Stat Increase")
        self.nex = choose_type(self.scan,self.root)
    def encode(self) -> str:
        line = self.link + self.type +":"+str(int(self.isSkill)) +":" + self.toIncrease + ":" + str(self.amt) + "\n"
        dprint(line)
        line += self.nex.encode()
        return line

class Toggle_Flag(MicroEvent):
    def parse(self):
        #syntax
        #fla:flag:on or off
        par=self.line.split(":")
        self.type = par[0]
        self.flag = par[1]
        self.on = ("1" == par[2]) #True is on, soooo...
        #get next
        self.nex = choose_type(self.scan,self.root)
    def encode(self) -> str:
        line = self.link + self.type +":" + self.flag + ":" + str(int(self.on)) + "\n"
        dprint(line)
        line+=self.nex.encode() 
        return line
#Discard a skill card
class Discard(MicroEvent):
    def parse(self):
        #syntax
        #dis:card
        par = self.line.split(":")
        self.type = par[0]
        self.card = par[1]
        dprint("Parsed discard")
        self.nex = choose_type(self.scan,self.root)
    def encode(self) -> str:
        line = self.link + self.type + ":" + self.card +"\n"
        dprint(str(self.nex))
        line+=self.nex.encode() 
        return line

#MicroEvent that sends you back to a link tag
class Link(MicroEvent):
    def parse(self):
        par = self.line.split(":")
        self.type = par[0]
        self.key = par[1]
        self.nex = self.root.links[par[1]]
        dprint("link to \"" + par[1] + "\" successfully parsed!")  
    def encode(self) -> str:
        line = self.type + ":" + self.key + "\n"
        return line

def choose_type(scan, root) -> MicroEvent :
    line = scan.readline().split("\n")[0]
    linkless = line
    if "#\\#" in line:
        linkless = line.split("#\\#")[1]
    #there's no reason someone would link to end. 
    dprint("Read in line: \"" + line + "\"")
    typ = linkless.split(":")[0]
    if (typ == "end") : return End(line,scan, root)
    if (typ == "dia") : return Dialog(line, scan, root)
    if (typ == "que") : return Question(line, scan, root)
    if (typ == "cho") : return Choice(line, scan, root)
    if (typ == "cqu") : return CardQuestion(line, scan, root)
    if (typ == "car") : return Card(line, scan, root)
    if (typ == "fail") : return Fail(line, scan, root)
    if (typ == "inc") : return Increase(line, scan, root)
    if (typ == "dis") : return Discard(line, scan, root)
    if (typ == "lin") : return Link(line, scan, root)
    if (typ == "fla") : return Toggle_Flag(line, scan, root)

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
        self.root = EventRoot(scan, erinfo[0],erinfo[1])
        dprint("EventRoot parsed successfully!")
        scan.close()
        
        


