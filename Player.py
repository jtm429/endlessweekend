from EventFileParser import EventFileParser, dprint
import random
import Display
"""
Within the Model View Controller Design pattern player is now the controller
It manages player attributes flags and steps through events
"""


class player():
    def __init__(self, save=""):
 #new player if no save file
        if save == "" :
            save = "new.plr"
            dprint("new player file selected")
        f = open(save, "r")
        data = f.read().splitlines()
        f.close()
        dprint(data[0])
        self.days = int(data[0])
        dprint(data[1])
        self.attr = attributes(data[1])
        dprint(data[2])
        self.flags = data[2].split(":")
        self.hand = hand(self)
        self.disp = Display.TextDisplay(self)
        dprint("player data successfully parsed")
        
    def saveGame(self, filename):
        writ = open(filename, "w")
        writ.writeline(self.days)
        writ.writeline(self.attr)
        for i in range(len(self.flags)):
            writ.write(self.flags[i])
            if i <len(self.flags)-1:
                writ.write(":")
    def event_player(self, root):
        self.loc = root.location
        self.micro_router(root.MEroot)
    def toggle_flag(self, flag):
        if( flag in self.flags):
            self.flags.remove(flag)
        else :
            self.flags.append(flag)
    #routes microevents to the correct methods to play them
    def micro_router(self, mevent):
        dprint("noodles"+str(mevent))
        if not mevent.type == "end":
            new = self.disp.display(mevent)
            self.micro_router(new)

    #a conditional statement evaluator
    def condition_eval(self, who, cond):
        #the most common conditional exits out almost immediately
        if(cond == "") : return True
        #accounting for "&"
        elif "&" in cond : 
            condo = cond.split("&")
            a = True
            for c in condo :
                a = a & self.condition_eval(who, c)
            return a
        #accounting for "or"
        elif "|" in cond : 
            condo = cond.split("|")
            a = False
            for c in condo :
                a = a | self.condition_eval(who, c)
            return a
        #this should be formatted "<val" for example "<7" would mean the "who" skill need to be greater than 7
        #I might make less than possible at some point, but I'm not going to right now. 
        elif "<" in cond :
            compare = int(cond.split("<")[1])
            return (compare < self.attr.get_skill_value(who))
        #last one can only be flags at this point
        else : return cond in self.flags


class attributes():
    def __init__(self, save=""):
        asd = save.split(":")
        att = asd[0].split(",")
        #load stats
        self.stats = {"":0,"mind":int(att[0]), "body":int(att[1]), "soul":int(att[2]), "inwa":int(att[3]), "outw":int(att[4])}
        #load skills
        f = open("skills", "r")
        skinfo = f.read().splitlines()
        f.close()
        self.skills = {}
        #getting skills
        for ski in range(len(skinfo)) :
            name = skinfo[ski].split(":")[0]
            baseval = asd[1].split(",")[ski]
            self.skills.update({name:skill(skinfo[ski],baseval)})
    def __str__(self):
        ret = ""
        for key, value in self.stats:
            if key != "" & key != "outw": ret += str(value)+","
        ret+=self.stats["outw"]+":"
        for key, value in self.skills:
            if key != "agility" : ret+=str(value)+","
            else : ret+=str(value)
        return ret
    def get_skill_value(self, skill) -> int:
        return self.skills[skill].getVal(self)

    #returns amount of XP gained for skills and the increase amount for stats
    def stat_inc(self, mevent):
        if mevent.isSkill :
            dprint(str(self.skills))
            return self.skills[mevent.toIncrease].addXP(self.stats,mevent.amt)
        else :
            self.stats[mevent.toIncrease]+=mevent.amt
            return mevent.amt


class skill():
    def __init__(self, data, baseval):
        par = data.split(":")
        self.name = par[0]
        #parent attributes
        self.mom = par[1]
        self.dad = par[2]
        self.desc = par[3]
        spli = baseval.split(".")
        self.bval = int(spli[0])
        self.exp = int(spli[1])
        self.inc = 0
    #takes the attributes of the player and calculates their value. 
    def getVal(self, attr) -> int:
        sum = attr.stats[self.dad]+attr.stats[self.mom]+self.bval
        return sum
    def addXP(self, attr,baseXP):
        addy = baseXP*(attr[self.dad]+attr[self.mom])
        self.exp= self.exp + addy
        dprint("exp:"+str(self.exp))
        dprint("bval:"+str(self.bval))
        if (self.exp > 100*(self.bval)and self.bval != 0) or (self.bval == 0 and self.exp > 100) :
            
            self.exp-=(100*self.bval)
            self.bval+=1
            self.inc = 1
        return addy
#hand of cards class
class hand():
    def __init__(self, plyr):
        self.cards = []
        self.deck = []
        dprint(str(plyr.attr.skills))
        for key, val in plyr.attr.skills.items():
            self.deck.append(key)
    def add_card(self, card):
        self.cards.append(card)
    def draw_card(self):
        #selecting random card
        rand = random.randrange(len(self.deck))
        card = self.deck.pop(rand)
        self.cards.append(card)
        return card
    def discard_card(self, card):
        if card in self.cards :
            self.cards.remove(card)
            if card not in self.deck :
                self.deck.append(card)
    def discard_all(self):
        cards = self.cards
        for card in cards :
            self.discard_card(card)
    def draw_hand(self, handsize=7):
        self.discard_all()
        for i in range(handsize):
            self.draw_card()


        




