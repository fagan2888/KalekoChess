#This class holds a list of FEN strings, one corresponding to each move
#The GUI has a "back" button to return to the previous move... that's where
#this class comes in handy


FEN_STARTING = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

class MoveLogger():

    #Here's the list (global)
    moves = []

    def __init__(self):
        self.moves.append(FEN_STARTING)

    #Add a move to the list
    def AddMove(self,fenstring):
        self.moves.append(fenstring)

    #Return the last move, and remove most recent from list
    #(-1 is the current move, -2 is the move before that)
    def LastMove(self):
        lastmove = self.moves[-2]
        del self.moves[-1]
        return lastmove

    #Return a specific move number in the list
    def SpecificMove(self,movenumber):
        pass
