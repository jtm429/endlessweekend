from EventFileParser import EventFileParser, dprint

class player():
    def __init__(self, save=""):
 #new player if no save file
        if save == "" :
            save = "new.plr"
            dprint("new player file selected")
        f = open(save, "r")
        data = f.read().splitlines()
        f.close()
        self.days = int(data[0])
        self.attr = attributes(data[1])
        self.flags = data[2].split(":")
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
    #routes microevents to the correct methods to play them
    def micro_router(self, mevent):
        if mevent.type = "dia" : play_dia(mevent)
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
            return (compare < self.attr.skills[who].getVal())
        #last one can only be flags at this point
        else : return cond in self.flags

    def play_dia(self,mevent):
        if(self.condition_eval(mevent.who, mevent.con)):
            if(mevent.who != "") : print(mevent.who+":")
            if(mevent.emo != "") : print("<"+mevent.emo+">")
            print(mevent.text)
        
        


        

class attributes():
    def ___init__(self, save=""):
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
    #takes the attributes of the player and calculates their value. 
    def getVal(self, attr) -> int:
        sum = attr[self.dad]+attr[self.mom]+self.bval
        return sum
    def addXP(self, attr,baseXP):
        addy = baseXP*(attr[self.dad]+attr[self.mom])
        self.exp= self.exp + addy
        if self.exp > 100*self.bval :
            self.exp-=(100*self.bval)
            self.bval+=1




