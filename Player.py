from EventFileParser import EventFileParser, dprint

class player():
    def __init__(self, save=""):
 #new player if no save file
        if save == "" :
            save = "new.plr"
        f = open(save, "r")
        data = f.read().splitlines()
        f.close()
        self.days = int(data[0])
        self.attr = attributes(data[1])
        self.flags = data[2].split(":")
    #plays an event
    def play_event(self, file):




        

class attributes():
    def ___init__(self, save=""):
        asd = save.split(":")
        att = asd[0].split(",")
        #load stats
        self.stats = {"":0"mind":int(att[0]), "body":int(att[1]), "soul":int(att[2]), "inwa":int(att[3]), "outw":int(att[4])}
        #load skills
        f = open("skills", "r")
        skinfo = f.read().splitlines()
        f.close()
        self.skills = {}
        for ski=0 in len(skinfo) :
            name = skinfo[ski].split(":")[0]
            baseval = asd[1].split(",")[ski]
            self.skills.update(name:skill(skinfo[ski],baseval))



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
    def getVal(self, attr):
    sum = attr[self.dad]+attr[self.mom]+self.bval
    return sum
    #adds experience to raise base value and level up the skill
    def addXP(self, attr,baseXP):
        addy = baseXP*(attr[self.dad]+attr[self.mom])
        self.exp= self.exp + addy
        if self.exp > 100*self.bval :
            self.exp-=(100*self.bval)
            self.bval+=1
    #declaring str method
    def __str__(self) -> str:
        return str(self.bval) +"."+str(self.exp)




