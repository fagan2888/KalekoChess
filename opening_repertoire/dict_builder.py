#Here's the repertoire dictionary (global)
repertoire = {}

class Repertoire():

    #Repertoire dictionary:
    #Key is FEN string, element is tuple that holds (the next move, the comments)
    def __init__(self):
        self.BuildDictFromFile(self)
        #self.PrintDict(repertoire)

    def SearchDict(self,fenstring):
#        print "DEBUG: Searching dictionary for ",fenstring        
        
        default = ("DNE","DNE")
        return repertoire.get(fenstring,default)

    def AddToDict(self, mydict, fenstring, move, comments):
        mydict[fenstring]=(move,comments)

    def PrintDict(self,dictionary):
        print "\n----- PRINTING REPERTOIRE DICTIONARY -----\n"
        for key in dictionary.keys():
            print "Dictionary['%s'] = %s" % (key,dictionary[key])
        print "\n------------------------------------------\n"
    
    def BuildDictFromFile(self,filename):

        #Read in the file
        with open("opening_repertoire/test_rep.txt") as f:
            content = f.readlines()

        #Loop through the lines of the file (already read in) and 
        #add them to the dictionary
        for line in content:
            myfen = line.strip().split("|")[0]
            mynextmove = line.strip().split("|")[1]
            mycomments = line.strip().split("|")[2]
            
            #Add this line's information to the dictionary
            self.AddToDict(repertoire,myfen,mynextmove,mycomments)

        return repertoire
