# sends a HTTP request and gets a response

import httplib
import sys
import HTMLParser

url = sys.argv[1]
conn = httplib.HTTPConnection(url)
conn.request("GET", "")
r1 = conn.getresponse()

res = r1.read()


