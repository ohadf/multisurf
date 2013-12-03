import httplib
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import sys

class MyHTMLParser(HTMLParser):
    def __init__(self, s):
        HTMLParser.__init__(self)
        self.results = s
    def handle_starttag(self, tag, attrs):
        self.results = self.results + "Start tag: " + tag + "\n"
        for attr in attrs:
            self.results = self.results + "     attr:" + str(attr) + "\n"
    def handle_endtag(self, tag):
        self.results = self.results + "End tag  :" + tag + "\n"
    def handle_data(self, data):
        self.results = self.results + "Data     :" + data + "\n"
    def handle_comment(self, data):
        self.results = self.results + "Comment  :" + data + "\n"
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        self.results = self.results + "Named ent:" + c + "\n"
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        self.results = self.results + "Num ent  :" + c + "\n"
    def handle_decl(self, data):
        self.results = self.results + "Decl     :" + data + "\n"

parse_results1 = ""
parser1 = MyHTMLParser(parse_results1)

parse_results2 = ""
parser2 = MyHTMLParser(parse_results2)

url1 = sys.argv[1]
conn1 = httplib.HTTPConnection(url1)
conn1.request("GET", "")
r1 = conn1.getresponse()

url2 = sys.argv[2]
conn2 = httplib.HTTPConnection(url2)
conn2.request("GET", "")
r2 = conn2.getresponse()

respMsg1 = r1.read()
respMsg2 = r2.read()

parser1.feed(respMsg1)
parse_lines1 = parser1.results.split("\n")
parser2.feed(respMsg2)
parse_lines2 = parser2.results.split("\n")

if parse_lines1 == parse_lines2:
    print "EQUAL"
else:
    print "NOT EQUAL"

# things that can be different are in white list.  everything else should be the same
white_list = []

current_start = ""

# requires both requests to have the same number of lines
for i in range(0, (len(parse_lines1)-1)):
    if "Start tag" in parse_lines1[i]:
        n = parse_lines1[i].split(':')[1].strip()
        current_start = n
        #print "start" + "     *" + n +"*"
    if "End tag" in parse_lines1[i]:
        n = parse_lines1[i].split(':')[1].strip()
        #print "end" + "     *" + n +"*"
    if "Data" in parse_lines1[i]:
        if not current_start in white_list:
            if parse_lines1[i] != parse_lines2[i]:
                print "DATA LINES NOT EQUAL"
                print parse_lines1[i]
                print parse_lines2[i]
    if "Comment" in parse_lines1[i]:
        if not current_start in white_list:
            if parse_lines1[i] != parse_lines2[i]:
                print "COMMENT LINES NOT EQUAL"
                print parse_lines1[i]
                print parse_lines2[i]
    if "Decl" in parse_lines1[i]:
        if not current_start in white_list:
            if parse_lines1[i] != parse_lines2[i]:
                print "DECL LINES NOT EQUAL"
                print parse_lines1[i]
                print parse_lines2[i]
    if "Named ent" in parse_lines1[i]:
        if not current_start in white_list:
            if parse_lines1[i] != parse_lines2[i]:
                print "NAMED ENT LINES NOT EQUAL"
                print parse_lines1[i]
                print parse_lines2[i]
    if "Num ent" in parse_lines1[i]:
        if not current_start in white_list:
            if parse_lines1[i] != parse_lines2[i]:
                print "NUM ENT LINES NOT EQUAL"
                print parse_lines1[i]
                print parse_lines2[i]
    if "attr:" in parse_lines1[i]:
        if not current_start in white_list:
            if parse_lines1[i] != parse_lines2[i]:
                print "ATTR LINES NOT EQUAL"
                print parse_lines1[i]
                print parse_lines2[i]
