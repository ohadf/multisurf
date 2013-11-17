import httplib
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import sys

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Start tag:", tag
        for attr in attrs:
            print "     attr:", attr
    def handle_endtag(self, tag):
        print "End tag  :", tag
    def handle_data(self, data):
        print "Data     :", data
    def handle_comment(self, data):
        print "Comment  :", data
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        print "Named ent:", c
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        print "Num ent  :", c
    def handle_decl(self, data):
        print "Decl     :", data

parser = MyHTMLParser()

for x in name2codepoint:
    print x

#url1 = sys.argv[1]
#conn1 = httplib.HTTPConnection(url1)
#conn1.request("GET", "")
#r1 = conn1.getresponse()

#url2 = sys.argv[2]
#conn2 = httplib.HTTPConnection(url2)
#conn2.request("GET", "")
#r2 = conn2.getresponse()

#respMsg1 = r1.read()
#respMsg2 = r2.read()

#msg1 = respMsg1.splitlines()
#msg2 = respMsg2.splitlines()

#parser.feed(respMsg1)

print "Done!"

#for line in range (0, len(msg1)):
  #  if msg1[line] != msg2[line]:
    #print "requests did not match at line %d: " % line
    #print msg1[line]
      #  print msg2[line]
        #break

#print("finished comparing")
