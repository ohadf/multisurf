import httplib
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import sys

class MyHTMLParser(HTMLParser):
    def __init__(self, s):
        HTMLParser.__init__(self)
        self.results = s
    def handle_starttag(self, tag, attrs):
        #print "Start tag:", tag
        self.results = self.results + "Start tag: " + tag + "\n"
        for attr in attrs:
            #print "     attr:", attr
            self.results = self.results + "     attr:" + str(attr) + "\n"
    def handle_endtag(self, tag):
        #print "End tag  :", tag
        self.results = self.results + "End tag  :" + tag + "\n"
    def handle_data(self, data):
        #print "Data     :", data
        self.results = self.results + "Data     :" + data + "\n"
    def handle_comment(self, data):
        #print "Comment  :", data
        self.results = self.results + "Comment  :" + data + "\n"
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        #print "Named ent:", c
        self.results = self.results + "Named ent:" + c + "\n"
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        #print "Num ent  :", c
        self.results = self.results + "Num ent  :" + c + "\n"
    def handle_decl(self, data):
        #print "Decl     :", data
        self.results = self.results + "Decl     :" + data + "\n"

parse_results = ""
parser = MyHTMLParser(parse_results)

url1 = sys.argv[1]
conn1 = httplib.HTTPConnection(url1)
conn1.request("GET", "/~melara/index.html")
r1 = conn1.getresponse()

url2 = sys.argv[2]
conn2 = httplib.HTTPConnection(url2)
conn2.request("GET", "")
r2 = conn2.getresponse()

respMsg1 = r1.read()
respMsg2 = r2.read()

#msg1 = respMsg1.splitlines()
#msg2 = respMsg2.splitlines()

parser.feed(respMsg1)

print parser.results

#for line in range (0, len(msg1)):
  #  if msg1[line] != msg2[line]:
    #print "requests did not match at line %d: " % line
    #print msg1[line]
      #  print msg2[line]
        #break

#print("finished comparing")
