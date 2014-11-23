from itertools import groupby
from copy import deepcopy

import pieces
import re

class ChessError(Exception): pass
class InvalidCoord(ChessError): pass
class InvalidColor(ChessError): pass
class InvalidMove(ChessError): pass
class Check(ChessError): pass
class CheckMate(ChessError): pass
class Draw(ChessError): pass
class NotYourTurn(ChessError): pass

FEN_STARTING = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
RANK_REGEX = re.compile(r"^[A-Z][1-8]$")

class Board(dict):
    '''
       Board

       A simple chessboard class

       TODO:

        * PGN export
        * En passant
        * Castling
        * Promoting pawns
        * Fifty-move rule
    '''

    axis_y = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
    axis_x = tuple(range(1,9)) # (1,2,3,...8)

    captured_pieces = { 'white': [], 'black': [] }
    player_turn = None

    #castling availability. If neither side can castle, this is "-". Otherwise, this has one or more letters: "K" (White can castle kingside), "Q" (White can castle queenside), "k" (Black can castle kingside), and/or "q" (Black can castle queenside).
    castling = 'KQkq'
    en_passant = '-'
    halfmove_clock = 0
    fullmove_number = 1
    history = []
    isFlipped = False

    def __init__(self, fen = None):
        if fen is None: self.load(FEN_STARTING)
        else: self.load(fen)

    def __getitem__(self, coord):
        if isinstance(coord, str):
            coord = coord.upper()
            if not re.match(RANK_REGEX, coord.upper()): raise KeyError
        elif isinstance(coord, tuple):
            coord = self.letter_notation(coord)
        try:
            return super(Board, self).__getitem__(coord)
        except KeyError:
            return None

    def save_to_file(self): pass

    def is_in_check_after_move(self, p1, p2):
        # Create a temporary board
        tmp = deepcopy(self)
        tmp._do_move(p1,p2,False,False)
        return tmp.is_in_check(self[p1].color)

    def move(self, p1, p2):
        p1, p2 = p1.upper(), p2.upper()
        piece = self[p1]
        dest  = self[p2]
        is_castling_kingside = False
        is_castling_queenside = False


        if self.player_turn != piece.color:
            raise NotYourTurn("Not " + piece.color + "'s turn!")

        enemy = self.get_enemy(piece.color)
        possible_moves = piece.possible_moves(p1)
        
        #if board is flipped, flip all possible moves
        if self.isFlipped:
            for x in xrange(len(possible_moves)):
                possible_moves[x]=self.flip_coord(possible_moves[x])

        # 0. Check if p2 is in the possible moves
        if p2 not in possible_moves:
            raise InvalidMove

        # If enemy has any moves look for check
        if self.all_possible_moves(enemy):
            if self.is_in_check_after_move(p1,p2):
                raise Check

        #Check if it's castling
        if piece.color == 'white' and p1 == 'E1' and p2 == 'G1':
            is_castling_kingside = True
        if piece.color == 'black' and p1 == 'E8' and p2 == 'G8':
            is_castling_kingside = True
        if piece.color == 'white' and p1 == 'E1' and p2 == 'C1':
            is_castling_queenside = True
        if piece.color == 'black' and p1 == 'E8' and p2 == 'C8':
            is_castling_queenside = True
            
        if not possible_moves and self.is_in_check(piece.color):
            raise CheckMate
        elif not possible_moves:
            raise Draw
        else:
            self._do_move(p1, p2, is_castling_kingside, is_castling_queenside)
            self._finish_move(piece, dest, p1,p2)

    def get_enemy(self, color):
        if color == "white": return "black"
        else: return "white"

    def _do_move(self, p1, p2, is_castling_kingside, is_castling_queenside):
        '''
            Move a piece without validation
        '''
        piece = self[p1]
        dest  = self[p2]
        
        del self[p1]
        self[p2] = piece
        
        #if is_castling_kingside, move the rook too
        if is_castling_kingside:
            if piece.color == 'white':
                self._do_move('H1','F1',False,False)
            if piece.color == 'black':
                self._do_move('H8','F8',False,False)
        if is_castling_queenside:
            if piece.color == 'white':
                self._do_move('A1','D1',False,False)
            if piece.color == 'black':
                self._do_move('A8','D8',False,False)
        

    def _finish_move(self, piece, dest, p1, p2):
        '''
            Set next player turn, count moves, log moves, etc.
        '''
        enemy = self.get_enemy(piece.color)
        if piece.color == 'black':
            self.fullmove_number += 1
        self.halfmove_clock +=1
        self.player_turn = enemy
        abbr = piece.abbriviation
        if abbr == 'P':
            # Pawn has no letter
            abbr = ''
            # Pawn resets halfmove_clock
            self.halfmove_clock = 0
        if dest is None:
            # No capturing
            movetext = abbr +  p2.lower()
        else:
            # Capturing
            movetext = abbr + 'x' + p2.lower()
            # Capturing resets halfmove_clock
            self.halfmove_clock = 0

        self.history.append(movetext)


    def all_possible_moves(self, color):
        '''
            Return a list of `color`'s possible moves.
            Does not check for check.
        '''

        if(color not in ("black", "white")): raise InvalidColor
        result = []
        for coord in self.keys():
            #if flipped, flip coord:
            if self.isFlipped:
                coord = self.flip_coord(coord)
            
            if (self[coord] is not None) and self[coord].color == color:
                moves = self[coord].possible_moves(coord)
                #if board is flipped, flip all possible moves
                if self.isFlipped:
                    for x in xrange(len(moves)):
                        moves[x]=self.flip_coord(moves[x])

                if moves: result += moves
        return result

    def occupied(self, color):
        '''
            Return a list of coordinates occupied by `color`
        '''
        result = []
        if(color not in ("black", "white")): raise InvalidColor

        for coord in self:
            #if board is flipped, flip coord
#            if self.isFlipped:
#                coord=self.flip_coord(coord)
            
            if self[coord].color == color:
                result.append(coord)
        return result

    def is_king(self, piece):
        return isinstance(piece, pieces.King)


    def get_king_position(self, color):
        for pos in self.keys():
            if self.is_king(self[pos]) and self[pos].color == color:
                return pos

    def get_king(self, color):
        if(color not in ("black", "white")): raise InvalidColor
        return self[self.get_king_position(color)]

    def is_in_check(self, color):
        if(color not in ("black", "white")): raise InvalidColor
        king = self.get_king(color)
        enemy = self.get_enemy(color)
        return king in map(self.__getitem__, self.all_possible_moves(enemy))

    def letter_notation(self,coord):
        if not self.is_in_bounds(coord): return
        
        result = self.axis_y[coord[1]] + str(self.axis_x[coord[0]])
        try:
            if not self.isFlipped:
                return result
            else:
                return self.flip_coord(result)
        except IndexError:
            raise InvalidCoord

    def letter_notation_flip_independent(self,coord):
        if not self.is_in_bounds(coord): return
        try:
                return self.axis_y[coord[1]] + str(self.axis_x[coord[0]])
        except IndexError:
            raise InvalidCoord

    def number_notation(self, coord):
        return int(coord[1])-1, self.axis_y.index(coord[0])
        
    def is_in_bounds(self, coord):
        if coord[1] < 0 or coord[1] > 7 or\
           coord[0] < 0 or coord[0] > 7:
            return False
        else: return True

    def load(self, fen):
        '''
            Import state from FEN notation
        '''
        self.clear()
        # Split data
        fen = fen.split(' ')
        # Expand blanks
        def expand(match): return ' ' * int(match.group(0))

        fen[0] = re.compile(r'\d').sub(expand, fen[0])

        for x, row in enumerate(fen[0].split('/')):
            for y, letter in enumerate(row):
                if letter == ' ': continue
                coord = self.letter_notation((7-x,y))
                self[coord] = pieces.piece(letter)
                self[coord].place(self)

        if fen[1] == 'w': self.player_turn = 'white'
        else: self.player_turn = 'black'

        self.castling = fen[2]
        self.en_passant = fen[3]
        self.halfmove_clock = int(fen[4])
        self.fullmove_number = int(fen[5])

    def export(self):
        '''
            Export state to FEN notation
        '''
        def join(k, g):
            if k == ' ': return str(len(g))
            else: return "".join(g)

        def replace_spaces(row):
            # replace spaces with their count
            result = [join(k, list(g)) for k,g in groupby(row)]
            return "".join(result)


        result = ''
        for number in self.axis_x[::-1]:
            for letter in self.axis_y:
                piece = self[letter+str(number)]
                if piece is not None:
                    result += piece.abbriviation
                else: result += ' '
            result += '/'

        result = result[:-1] # remove trailing "/"
        result = replace_spaces(result)

        #check if castling is ok
        self.update_castling()

        result += " " + (" ".join([self.player_turn[0],
                         self.castling,
                         self.en_passant,
                         str(self.halfmove_clock),
                         str(self.fullmove_number)]))
        return result

    def can_castle_kingside(self, color):
        if(color not in ("black", "white")): raise InvalidColor

        #Is the king not on his home square?
        if color == "white" and self.get_king_position(color) != "E1":
            return False
        if color == "black" and self.get_king_position(color) != "E8":
            return False
        
        #Is the rook not still on his home square?
        #IMPLEMENT THIS
        
        #Are there any pieces (of any color) blocking the castling squares?
        blocked = self.occupied('white') + self.occupied('black')
        if color == "white" and 'F1' in blocked:
            return False
        if color == "white" and 'G1' in blocked:
            return False
        if color == "black" and 'F8' in blocked:
            return False
        if color == "black" and 'G8' in blocked:
            return False

        #Are any of the castling squares controlled by the enemy?
        #IMPLEMENT THIS

        #Has the king moved, or has the rook moved
        #IMPLEMENT THIS

        return True


    def can_castle_queenside(self, color):

        if(color not in ("black", "white")): raise InvalidColor

        #Is the king not on his home square?
        if color == "white" and self.get_king_position(color) != "E1":
            return False
        if color == "black" and self.get_king_position(color) != "E8":
            return False
        
        #Is the rook not still on his home square?
        #IMPLEMENT THIS
        
        #Are there any pieces (of any color) blocking the castling squares?
        blocked = self.occupied('white') + self.occupied('black')
        if color == "white" and 'B1' in blocked:
            return False
        if color == "white" and 'C1' in blocked:
            return False
        if color == "white" and 'D1' in blocked:
            return False
        if color == "black" and 'B8' in blocked:
            return False
        if color == "black" and 'C8' in blocked:
            return False
        if color == "black" and 'D8' in blocked:
            return False

        #Are any of the castling squares controlled by the enemy?
        #IMPLEMENT THIS

        #Has the king moved, or has the rook moved
        #IMPLEMENT THIS

        return True

    def update_castling(self):

    #apparently, in FEN strings, the starting position has KQkq
    #meaning both sides can castle both ways
    #even though in that precise position, neither is possible
    #this function should be implemented like...
    #if white's H1 rook has moved, "K" is no longer in castling string
    #if white's king has moved, "KQ" are both no longer in castling string
    #etc.

    #this is wrong:
#        self.castling = ""
#        if self.can_castle_kingside('white'):
#            self.castling = self.castling + "K"
#        if self.can_castle_queenside('white'):
#            self.castling = self.castling + "Q"
#        if self.can_castle_kingside('black'):
#            self.castling = self.castling + "k"
#        if self.can_castle_queenside('black'):
#            self.castling = self.castling + "q"

        #for now, just always assume castling is a possibility
        self.castling = 'KQkq'

    def set_isflipped(self,isflipped):
        self.isFlipped = isflipped

    def flip_coord(self,coord):
        return self.axis_y[7-self.axis_y.index(coord[0])]+str(self.axis_x[8-int(coord[1])])
