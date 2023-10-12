import EventFileParser as eve
def boxer(txt):
    lines = txt.split("\n")
    length = 0
    for line in lines :
        if len(line) > length :
            length = len(line)
    newli = "┌"
    for i in range(length):
        newli += "─"
    newli += "┐\n"
    for line in lines :
        newli += "│" +line 
        for i in range(len(line),length):
            newli+=" "
        newli += "│\n"
    newli += "└"
    for i in range(length):
        newli += "─"
    newli += "┘\n"
    return newli

def disval_dia(me : eve.Dialog, top=True):
    line = "type        : " + me.type  + "\n"
    line += "who         : " + me.who  + "\n"
    line += "conditional : " + me.con  + "\n"
    line += "emotion     : " + me.emo  + "\n"
    line += "text        : " + me.text + "\n"
    if top :
        line += "next:\n"
        line += display_vals(me.nex, False)
        print(boxer(line))
    return boxer(line)
def disval_que(me : eve.Question, top=True):
    line = "type        : " + me.type  + "\n"
    line += "who         : " + me.who  + "\n"
    line += "conditional : " + me.con  + "\n"
    line += "emotion     : " + me.emo  + "\n"
    line += "text        : " + me.text + "\n"
    if top :
        i = 0
        for cho in me.choices :
            line += "choice {i}:\n"
            line += display_vals(cho, False)
            i+=1
        print(boxer(line))
    return boxer(line)
def disval_cho(me : eve.Choice, top=True):
    line = "type        : " + me.type  + "\n"
    line += "who         : " + me.who  + "\n"
    line += "conditional : " + me.con  + "\n"
    line += "text        : " + me.text + "\n"
    if top :
        line += "next:\n"
        line += display_vals(me.nex, False)
    print(boxer(line))
    return boxer(line)
def disval_cqu(me : eve.CardQuestion, top=True):
    line =  "type        : " + me.type  + "\n"
    line += "who         : " + me.who  + "\n"
    line += "text        : " + me.text + "\n"
    if top :
        liner = ""
        for card, cho in me.choices :
            liner += "choice {card}:{cho.text}\n"
        line+=boxer(liner)
        print(boxer(line))
    return boxer(line)
def disval_car(me : eve.Card, top=True):
    line = "type        : " +me.type + "\n"
    line += me.card + " is "
    if not me.isProvided : line += "not " 
    line += "provided\n"
    line += "conditional : " + me.con  + "\n" 
    line += "text        : " + me.text + "\n" 
    if top :
        line += "next:\n"
        line += display_vals(me.nex, False)
        line += display_vals(me.fail, False)
        print(boxer(line))
    return boxer(line)
def disval_fai(me : eve.Fail, top=True):
    line = "type        : " +me.type + "\n"
    line += "text        : " + me.text + "\n" 
    if top :
        line += "next:\n"
        line += display_vals(me.nex, False)
        print(boxer(line))
    return boxer(line)
def disval_end(me : eve.End, top=True):
    line = "type        : " +me.type + "\n"
    line += "end         : " + me.end + "\n" 
    if top :
        print(boxer(line))
    return boxer(line)
def disval_inc(me : eve.Increase, top=True):
    line = "type        : " +me.type + "\n"
    line += "isSkill     : " + me.isSkill + "\n" 
    line += "toIncrease  : " + me.toIncrease + "\n" 
    line += "amount      : " + me.amt + "\n" 
    if top :
        line += "next:\n"
        line += display_vals(me.nex, False)
        print(boxer(line))
    return boxer(line)
def disval_fla(me : eve.Toggle_Flag, top=True):
    line = "type        : " +me.type + "\n"
    line += "flag id     : " + me.flag + "\n" 
    line += "on (or off) : " + me.on + "\n" 
    if top :
        line += "next:\n"
        line += display_vals(me.nex, False)
        print(boxer(line))
    return boxer(line)
def disval_dis(me : eve.Discard, top=True):
    line = "type        : " +me.type + "\n"
    line += "toDiscard   : " + me.card + "\n" 
    if top :
        line += "next:\n"
        line += display_vals(me.nex, False)
        print(boxer(line))
    return boxer(line)
def disval_lin(me : eve.Link, top=True):
    line = "type        : " +me.type + "\n"
    line += "link key    : " + me.key + "\n" 
    if top :
        line += "next:\n"
        line += display_vals(me.nex, False)
        print(boxer(line))
    return boxer(line)






def display_vals(mevent : eve.MicroEvent, top = True):
    vlas = "error"
    if mevent.type == "dia" :vlas = disval_dia(mevent,top)
    if mevent.type == "que" :vlas = disval_que(mevent, top)
    if mevent.type == "cho" :vlas = disval_cho(mevent, top)
    if mevent.type == "cqu" :vlas = disval_cqu(mevent, top)
    if mevent.type == "car" :vlas = disval_car(mevent, top)
    if mevent.type == "fail":vlas = disval_fai(mevent, top)
    if mevent.type == "end" :vlas = disval_end(mevent, top)
    if mevent.type == "inc" :vlas = disval_inc(mevent, top)
    if mevent.type == "fla" :vlas = disval_fla(mevent, top)
    if mevent.type == "dis" :vlas = disval_dis(mevent, top)
    if mevent.type == "lin" :vlas = disval_lin(mevent, top)
    return vlas
def get_children(mevent : eve.MicroEvent):
    
    pass

class EventEditor():
    def __init__(self, filename):
        file = eve.EventFileParser(filename)
        file.parse()
        self.root = file.root
        self.sel = self.root.MEroot
        self.children = get_children(self.sel)
