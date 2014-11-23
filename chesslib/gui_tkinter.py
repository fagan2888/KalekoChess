import os

import board
import pieces
import repertoire
import Tkinter as tk
import tkFileDialog as tkfd
import tkSimpleDialog as tksd

from PIL import Image, ImageTk

class BoardGuiTk(tk.Frame):
    
    myrep = repertoire.Repertoire()
 
    pieces = {}
    selected = None
    selected_piece = None
    hilighted = None
    icons = {}

    color1 = "white"
    color2 = "grey"

    rows = 8
    columns = 8

    @property
    def canvas_size(self):
        return (self.columns * self.square_size,
                self.rows * self.square_size)

    def __init__(self, parent, chessboard, square_size=64):

        self.isFlipped = False

        self.chessboard = chessboard
        self.square_size = square_size
        self.parent = parent

        self.current_status = tk.StringVar()
        self.current_status.set("White's Turn")
        
        canvas_width = self.columns * square_size
        canvas_height = self.rows * square_size

        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, background="grey")
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)

        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.bind("<Button-1>", self.click)

        self.statusbar = tk.Frame(self, height=128)
        self.statusbar.grid(row=3,column=0,columnspan=2)

        self.button_new = tk.Button(self.statusbar, text="Restart", fg="black", command=self.reset).grid(row=0,column=0)
        #self.label_status = tk.Label(self.statusbar, text="   White's turn  ", fg="black").grid(row=0,column=1)
        self.label_status = tk.Label(self.statusbar, textvariable=self.current_status, fg="black").grid(row=0,column=1)

        self.button_flip = tk.Button(self.statusbar, text="Flip Board", fg="black", command=self.flipboard).grid(row=0,column=2)
        self.button_quit = tk.Button(self.statusbar, text="Quit", fg="black", command=self.parent.destroy).grid(row=0,column=3)

        self.button_loadrep = tk.Button(self.statusbar, text="Load Repertoire", fg="black", command=self.init_repertoire).grid(row=1,column=0)
        self.button_addtorep = tk.Button(self.statusbar, text="Add to Repertoire", fg="black", command=self.add_to_repertoire).grid(row=1,column=1)
        self.button_checkrep = tk.Button(self.statusbar, text="Check Repertoire", fg="black", command=self.print_repertoire_info).grid(row=1,column=2)
        self.button_saverep = tk.Button(self.statusbar, text="Save Repertoire", fg="black", command=self.save_repertoire).grid(row=1,column=3)

        self.statusbar.pack(expand=False, fill="x", side='bottom')
        

    def click(self, event):

        # Figure out which square we've clicked
        col_size = row_size = event.widget.master.square_size

        current_column = event.x / col_size
        current_row = 7 - (event.y / row_size)

        position = self.chessboard.letter_notation((current_row, current_column))
        piece = self.chessboard[position]

        if self.selected_piece:
            self.move(self.selected_piece[1], position)
            self.selected_piece = None
            self.hilighted = None
            self.pieces = {}
            self.refresh()
            self.draw_pieces()

        self.hilight(position)
        self.refresh()

    def move(self, p1, p2):
        piece = self.chessboard[p1]
        dest_piece = self.chessboard[p2]
        
        if dest_piece is None or dest_piece.color != piece.color:
            try:
                self.chessboard.move(p1,p2)
            except board.ChessError as error:
                self.current_status.set(error.__class__.__name__)
            else:
                self.current_status.set(" " + piece.color.capitalize() +": "+ p1 + p2)


    def hilight(self, pos):
        piece = self.chessboard[pos]
        if piece is not None and (piece.color == self.chessboard.player_turn):
            self.selected_piece = (self.chessboard[pos], pos)
            self.hilighted = map(self.chessboard.number_notation, (self.chessboard[pos].possible_moves(pos)))

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.square_size) + int(self.square_size/2)
        y0 = ((7-row) * self.square_size) + int(self.square_size/2)

        #origin is upper left, positive x goes right, positive y goes down
        #upper right black rook is x0 = 480.000000, y0 = 32.000000
        #bottom left white rook is x0 = 32.000000, y0 = 480.000000
        if self.isFlipped:
            x0 = (8*self.square_size)-x0
            y0 = (8*self.square_size)-y0

        self.canvas.coords(name, x0, y0)

    def refresh(self, event={}):
        '''Redraw the board'''
        if event:
            xsize = int((event.width-1) / self.columns)
            ysize = int((event.height-1) / self.rows)
            self.square_size = min(xsize, ysize)

        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.square_size)
                y1 = ((7-row) * self.square_size)
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                if (self.selected is not None) and (row, col) == self.selected:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="orange", tags="square")
                elif(self.hilighted is not None and (row, col) in self.hilighted):
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="spring green", tags="square")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def draw_pieces(self):
        self.canvas.delete("piece")
        for coord, piece in self.chessboard.iteritems():
            x,y = self.chessboard.number_notation(coord)
            if piece is not None:
                filename = os.environ['KALEKOCHESS_TOP_DIR']+"/img/%s%s.gif" % (piece.color, piece.abbriviation.lower())
                piecename = "%s%s%s" % (piece.abbriviation, x, y)

                if(filename not in self.icons):
                    self.icons[filename] = ImageTk.PhotoImage(file=filename, width=32, height=32)

                self.addpiece(piecename, self.icons[filename], x, y)
                self.placepiece(piecename, x, y)

    def reset(self):
        self.chessboard.load(board.FEN_STARTING)
        self.refresh()
        self.draw_pieces()
        self.refresh()

    def flipboard(self):
        self.isFlipped = not self.isFlipped            
        self.refresh()

        

    def print_repertoire_info(self):
        repinfo = self.myrep.SearchDict(self.chessboard.export())
        if repinfo[0] == "DNE":
            print "Selected repertoire does not have a suggested move in this position."
        else:
            print "Repertoire recommends playing %s. Comments: %s" % (repinfo[0],repinfo[1])

    def init_repertoire(self):
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['initialdir'] = os.environ['KALEKOCHESS_TOP_DIR']+'/saved_repertoires/'
        options['initialfile'] = 'test_rep.txt'
        filename = tkfd.askopenfilename(**self.file_opt)

        if filename:
            self.myrep.BuildDictFromFile(filename)
        
    def add_to_repertoire(self):
        print "Add to repertoire"

        nextmove = tksd.askstring("Next Move","Enter next move:")
        comments = tksd.askstring("Comments","Enter comments:")
        self.myrep.AddToDict(self.chessboard.export(),nextmove,comments)
        
    def save_repertoire(self):
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['initialdir'] = os.environ['KALEKOCHESS_TOP_DIR']+'/saved_repertoires/'
        options['initialfile'] = 'test_rep.txt'
        outfname = tkfd.asksaveasfilename(**self.file_opt)

        if outfname:
            self.myrep.SaveDictToFile(filename=outfname)



def display(chessboard):
    root = tk.Tk()
    root.title("Simple Python Chess")

    gui = BoardGuiTk(root, chessboard)
    gui.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    gui.draw_pieces()

    #root.resizable(0,0)
    root.mainloop()

if __name__ == "__main__":
    display()
