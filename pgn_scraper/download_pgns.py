#To use this script, visit http://www.chessgames.com/ and type in some
#search info (player, opening, result, etc) to get a list of games
#(I could automate this but since I only plan to use this script a few
#times, I'm leaving this work up to the user)

#Usage: python download_pgns.py output_file_name.pgn
import sys

if len(sys.argv) != 2:
    print "Usage: python download_pgns.py output_file_name.pgn"
    quit()


import urllib2, re, BeautifulSoup

#Caro Kann games by Grischuk
#starting_url="http://www.chessgames.com/perl/chess.pl?yearcomp=exactly&year=&playercomp=black&pid=17279&player=&pid2=&player2=&movescomp=exactly&moves=&opening=B10-B19&eco=&result="

#Sicilian Najdorf games by Kasparov as Black, with Kasparov winning
starting_url="http://www.chessgames.com/perl/chess.pl?page=1&pid=15940&playercomp=black&eco=B90-B99&result=0-1"
n_pages_max = 10

gid_texts = []
for x in xrange(1,n_pages_max+1,1):
    new_url = starting_url.replace("page=1","page=%d"%x)
    print new_url
    req = urllib2.Request(new_url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    splitpage = the_page.split("\n")

    for item in splitpage:
        if "gid=" in item:
            if item not in gid_texts:
                gid_texts.append(item)


gids = []
for item in gid_texts:
    obj = re.search("gid=\d+",item)
    gid = obj.group().strip("gid=")
    gids.append(gid)

urls = []
url_base = "http://www.chessgames.com/perl/nph-chesspgn?text=1&gid="
for item in gids:
    urls.append(url_base+item)

outf = open(sys.argv[1],'w')

for url in urls:
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    text = BeautifulSoup.BeautifulSoup(the_page)
    outf.write(str(text))
    outf.write("\n\n")    

outf.close()
    
