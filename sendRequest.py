# sends a HTTP request and gets a response

import httplib
import sys

url = sys.argv[1]
conn = httplib.HTTPConnection(url)
conn.request("GET", "")
r1 = conn.getresponse()
