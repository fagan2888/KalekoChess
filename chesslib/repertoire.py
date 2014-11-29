#The opening repertoire is saved in terms of FEN strings.
#Each FEN string has an associated "nextmove" object with it.
#There will be a dict of { "FEN_STRING" : "nextmove" }
#The nextmove object should contain a string "move", and a string "comments"
#(nextmove.move, nextmove.comments)

#There will be a function to read in a text file repertoire into this dict.
#There will be a function to append to the dict.
#There will be a function to write the dict to a text file.



import os

#Here's the repertoire dictionary (global)
repertoire = {}

class Repertoire():

    #Repertoire dictionary:
    #Key is FEN string, element is tuple that holds (the next move, the comments)

    #Default file names and paths (overwritten when a repertoire is loaded)
    loaded_rep_filename = 'test_rep.txt'
    loaded_rep_filepath = os.environ['KALEKOCHESS_TOP_DIR']+'/saved_repertoires/'

    def __init__(self):
        self.hasLoadedDict = False
        #self.BuildDictFromFile(self)
        #self.PrintDict(repertoire)

    def SearchDict(self,fenstring):
#        print "DEBUG: Searching dictionary for ",fenstring        
        if not self.hasLoadedDict:
            print "WARNING! You're searching through a repertoire that hasn't been loaded from a file. Try using the \"Load Repertoire\" button."

        default = ("DNE","DNE")
        return repertoire.get(fenstring,default)

    def AddToDict(self, fenstring, move, comments):
        #Check if this fenstring already exists
        if fenstring in repertoire:
            print "UH OH ALREADY IN REPERTOIRE"
        else:
            repertoire[fenstring]=(move,comments)

    def PrintDict(self):
        print "\n----- PRINTING REPERTOIRE DICTIONARY -----\n"
        for key in repertoire.keys():
            print "Dictionary['%s'] = %s" % (key,dictionary[key])
        print "\n------------------------------------------\n"
    
    def BuildDictFromFile(self,filename):
        try:
            #Read in the file
            with open(filename,'r') as f:
                content = f.readlines()
        except IOError:
            print "Repertoire file %s does not exist." % filename

        self.loaded_rep_filename = os.path.basename(filename)
        self.loaded_rep_filepath = os.path.dirname(filename)

        #Loop through the lines of the file (already read in) and 
        #add them to the dictionary
        for line in content:
            myfen = line.strip().split("|")[0]
            mynextmove = line.strip().split("|")[1]
            mycomments = line.strip().split("|")[2]
            
            #Add this line's information to the dictionary
            self.AddToDict(myfen,mynextmove,mycomments)
        
        self.hasLoadedDict = True

        return repertoire

    def SaveDictToFile(self,filename):
        outf = open(filename,'w')
        for k in repertoire:
            outf.write("%s|%s|%s\n"%(k,repertoire[k][0],repertoire[k][1]))
        outf.close()

