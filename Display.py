import EventFileParser as eve
"""
This is intended to be the 'view' part of the Model-View-Controller design pattern
I'm going to make an abstract display class and the text implementation within this file.
In the future, I will make the graphical implementation, so I don't have to change the entire player class.
"""

class Displayer():
    #initializes the things required by the displayer
    def __init__(self, play):
        self.plyr = play 
    #this will take the place of my router in the original attempted implementation
    #returns the next event
    def display(self, event: eve.MicroEvent) -> eve.MicroEvent:
        if (event.type == "dia"): return self.display_dia(event)
        elif (event.type == "que"): return self.display_que(event)
        elif (event.type == "cqu"): return self.display_cqu(event)
        elif (event.type == "inc"): return self.display_inc(event)
        elif (event.type == "dis"): return self.display_dis(event)
        elif (event.type == "cho"): return self.display_cho(event)
        elif (event.type == "car"): return self.display_car(event)
        else : return self.handler(event)

    #display dialog
    def display_dia(self, event:eve.Dialog) -> eve.MicroEvent:
        pass
    #display question
    def display_que(self, event:eve.Question) -> eve.MicroEvent:
        pass
    #display card question
    def display_cqu(self, event:eve.CardQuestion) -> eve.MicroEvent:
        pass
    #display stat increase
    def display_inc(self, event:eve.Increase) -> eve.MicroEvent:
        pass
    #display discard
    def display_dis(self, event:eve.Discard) -> eve.MicroEvent:
        pass
    def display_cho(self, event:eve.Choice) -> eve.MicroEvent:
        pass
    def display_car(self, event:eve.Card) -> eve.MicroEvent:
        pass
    #handles events that dont display
    def handler(self,event) -> eve.MicroEvent:
        #this is a link
        if( event.type == "lin"): 
            #return next event
            return event.nex
        elif (event.typ == "fla"):
            #toggle flags
            if(event.flag in self.plyr.flags):
                if not event.on :
                    self.plyr.toggle_flag(event.flag)
            else :
                self.plyr.toggle_flag(event.flag)


            #return next event
            return event.nex


#text implementation of Displayer
class TextDisplay(Displayer):
    def display_dia(self, event) -> eve.MicroEvent:
        if(self.plyr.condition_eval(event.who, event.con)):
            if(event.who != "") : print(event.who+":")
            if (event.who in self.plyr.attr.skills): 
                print("["+event.who+"]: ",end="")
            else :
                print(event.who + ": ",end="")
            print(event.text)
            self.wait()

        return event.nex
    def wait(self):
            input("press Enter to continue...")

    def format_choice(self,mevent) -> str:
        #a choice should only have a who for a skill, you can't choose what someone else says.
        a = ""
        if(mevent.who != "") & (mevent.who in self.plyr.attr.skills): 
            a +="["+mevent.who+"]: "
        a+=mevent.text
        return a
    def display_que(self, event) -> eve.MicroEvent:
        if(self.plyr.condition_eval(event.who, event.con)):
            if(event.who != "" ):  
                if (event.who in self.plyr.attr.skills): 
                    print("["+event.who+"]: ",end="")
                else :
                    print(event.who + ": ",end="")
            if(event.emo != "") : print("<"+event.emo+"> ",end="")
            print(event.text)
            #now for the choices
            
            for cho in range(len(event.choices)) :
                a = str(cho)+": "+self.format_choice(event.choices[cho])
                print(a)
            ans = -1
            while  ans not in range(len(event.choices)):
                ansss = input("select an answer: ")
                try:
                    ans = int(ansss)
                except ValueError:
                    print("Invalid input: please input a number within range")
                eve.dprint(str(ans))

            return event.choices[ans]
        return event.nex
    #display card question
    def display_cqu(self, event) -> eve.MicroEvent:
        if(event.who != "" ):  
            print(event.who + ":")
        print(event.text+"\n")
        print("Hand:\n")
        
        #provide provided cards and populate choice list
        for card, micro in event.choices.items() :
            if micro.isProvided :
                self.plyr.hand.add_card(card)
            
        for choice in self.plyr.hand.cards :
            print("["+choice+"]"+event.choices[choice].text+"\n")
        ans = ""
        while ans not in self.plyr.hand.cards:
            ans = input("select an answer by typing the name of the skill: ")
        self.plyr.hand.discard_card(ans)
        return event.choices[ans]
    #card implementation
    #I realized I needed this because the card I sent back would be a card MicroEvent
    #Also they have a fail state
    def display_car(self, event: eve.Card) -> eve.MicroEvent:
        if self.plyr.condition_eval(event.card,event.con):
            print(event.text)
            return event.passed
        else :
            print(event.fail.text)
            return event.fail.nex
    #discard card implementation
    #this is more for the eventual graphical implementation
    #I think it'd be cool to have it fly back to the deck
    def display_dis(self, event) -> eve.MicroEvent:
        #discard card from hand
        self.plyr.hand.discard_card(event.card)
        print(event.card +" has been discarded")
        self.wait()
        return event.nex
    #display stat increase
    def display_inc(self, event) -> eve.MicroEvent:
        amt = self.plyr.attr.stat_inc(event)
        print(event.toIncrease + " has increased by "+ str(amt),end="")
        if(event.isSkill):
            print(" XP")
            a = self.plyr.attr.skills[event.toIncrease]
            if a.inc == 1 :
                print(event.toIncrease+" is now level "+ str(self.plyr.attr.get_skill_value(event.toIncrease)))
                a.inc = 0
        self.wait()
        return event.nex 
            
    def display_cho(self, event: eve.Choice) -> eve.MicroEvent:
        print(event.text)
        return event.nex