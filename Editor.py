import EventFileParser as eve
def boxer(txt):
    lines = txt.split("\n")
    length = 0
    for line in lines :
        if len(line) > length :
            length = len(line)
    newli = "┎"
    for i in range(length):
        newli += "─"
    newli += "┐"
def disval_dia(me : eve.Dialog):
    line = "type        : " + me.type
    line += "who         : " + me.who
    line += "conditional : " + me.con
    line += "emotion     : " + me.emo
    line += "text        : " + me.text
    print(line)
def disval_que(me : eve.Question):
    line = "type        : " + me.type  + "\n"
    line += "who         : " + me.who  + "\n"
    line += "conditional : " + me.con  + "\n"
    line += "emotion     : " + me.emo  + "\n"
    line += "text        : " + me.text + "\n"
    print(line)
def disval_cho(me : eve.choice):
    line = "type        : " + me.type  + "\n"
    line += "who         : " + me.who  + "\n"
    line += "conditional : " + me.con  + "\n"
    line += "text        : " + me.text + "\n"
    print(line)
def disval_cqu(me : eve.CardQuestion):
    line =  "type        : " + me.type  + "\n"
    line += "who         : " + me.who  + "\n"
    line += "text        : " + me.text + "\n"
    print(line)
def disval_car(me : eve.Card):
    line = "type        : " +me.type + "\n"
    line += me.card + " is "
    if not me.isProvided : line += "not " 
    line += "provided\n"
    line += "conditional : " + me.con  + "\n" 
    line += "text        : " + me.text + "\n" 



def display_vals(mevent : eve.MicroEvent):
    if mevent.type == "dia" : disval_dia(mevent)
    if mevent.type == "que" : disval_que(mevent)
    if mevent.type == "cho" : disval_cho(mevent)
    pass
def get_children(mevent : eve.MicroEvent):
    pass

class EventEditor():
    def __init__(self, filename):
        file = eve.EventFileParser(filename)
        file.parse()
        self.root = file.root
        self.sel = self.root.MEroot
        self.children = get_children(self.sel)
