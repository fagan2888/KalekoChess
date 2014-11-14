#repertoire dictionary:
#key is FEN string, element is tuple that holds (the next move, the comments)

#here's the dictionary
mydict = {}


def AddToDict(fenstring, move, comments):
    mydict[fenstring]=(move,comments)

def PrintDict(dictionary):
    for key in dictionary.keys():
        print "Dictionary['%s'] = %s" % (key,dictionary[key])
    

#Read in the file
with open("test_rep.txt") as f:
    content = f.readlines()


#Loop through the lines of the file (already read in) and add them to the dictionary
for line in content:
    myfen = line.strip().split("|")[0]
    mynextmove = line.strip().split("|")[1]
    mycomments = line.strip().split("|")[2]
    
    #Add this line's information to the dictionary
    AddToDict(myfen,mynextmove,mycomments)

#Print out the dictionary
PrintDict(mydict)
