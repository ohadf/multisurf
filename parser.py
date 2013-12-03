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

def parse(arg):
    parser = MyHTMLParser("")
    url = sys.argv[arg]
    conn = httplib.HTTPConnection(url)
    conn.request("GET", "")
    r = conn.getresponse()
    respMsg = r.read()
    parser.feed(respMsg)
    return parser.results.split("\n")

def check_equality(l1, l2, l3):
    if l1 == l2 == l3:
        print "EQUAL"
        return []
    else:
        print "NOT EQUAL"
        malicious_diff_lines = {}
        warning_diff_lines = {}
        for i in range(0, (len(parse_lines1)-1)):
            if (not parse_lines1[i] == parse_lines2[i]) and (parse_lines2[i] == parse_lines3[i]):
                malicious_diff_lines[i] = [parse_lines1[i], parse_lines2[i], parse_lines3[i]]
            elif (not parse_lines1[i] == parse_lines3[i]) and (parse_lines2[i] == parse_lines3[i]):
                malicious_diff_lines[i] = [parse_lines1[i], parse_lines2[i], parse_lines3[i]]
            elif (not parse_lines1[i] == parse_lines2[i]) and (not parse_lines1[i] == parse_lines3[i]) and (not parse_lines2[i] == parse_lines3[i]):
                warning_diff_lines[i] = [parse_lines1[i], parse_lines2[i], parse_lines3[i]]

        if not (len(malicious_diff_lines) == 0):
            print "MALICIOUS (...probably)"
            return [malicious_diff_lines, warning_diff_lines]
        if not (len(warning_diff_lines) == 0):
            print "WARNING"
            print warning_diff_lines
            return [warning_diff_lines]

parse_lines1 = parse(1)
parse_lines2 = parse(2)
parse_lines3 = parse(3)

check_equality(parse_lines1, parse_lines2, parse_lines3)
