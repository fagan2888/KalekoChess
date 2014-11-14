#Repertoire dictionary:
#Key is FEN string, element is tuple that holds (the next move, the comments)


def AddToDict(mydict, fenstring, move, comments):
    mydict[fenstring]=(move,comments)

def PrintDict(dictionary):
    print "\n----- PRINTING REPERTOIRE DICTIONARY -----\n"
    for key in dictionary.keys():
        print "Dictionary['%s'] = %s" % (key,dictionary[key])
    print "\n------------------------------------------\n"
    
def BuildDictFromFile(filename):

    #Here's the dictionary
    mydict = {}

    #Read in the file
    with open("test_rep.txt") as f:
        content = f.readlines()

    #Loop through the lines of the file (already read in) and add them to the dictionary
    for line in content:
        myfen = line.strip().split("|")[0]
        mynextmove = line.strip().split("|")[1]
        mycomments = line.strip().split("|")[2]
            
        #Add this line's information to the dictionary
        AddToDict(mydict,myfen,mynextmove,mycomments)

    return mydict


if __name__ == "__main__":
    repertoire = BuildDictFromFile("test_rep.txt")
    PrintDict(repertoire)
