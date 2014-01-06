import httplib
import sys

url1 = sys.argv[1]
conn = httplib.HTTPConnection(url1)
conn.request("GET", "")
r1 = conn.getresponse()

url2 = sys.argv[2]
conn = httplib.HTTPConnection(url2)
conn.request("GET", "")
r2 = conn.getresponse()

respMsg1 = r1.read()
respMsg2 = r2.read()

msg1 = respMsg1.splitlines()
msg2 = respMsg2.splitlines()

for line in range (0, len(msg1)):
    if msg1[line] != msg2[line]:
        print "requests did not match at line %d: " % line
        print msg1[line]
        print msg2[line]
        break

print("finished comparing")
    
