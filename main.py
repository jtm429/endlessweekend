from EventFileParser import EventFileParser
import Player

if __name__ == "__main__":
    a = EventFileParser("test.txt")
    a.parse()
    plyr = Player.player()
    plyr.event_player(a.root)
    exit()