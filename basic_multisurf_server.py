#Usage: python basic_multisurf_server.py <port>

import httplib
import socket
from OpenSSL import SSL
import OpenSSL
import util
import sys

context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('./certs/key-ohad.pem')
context.use_certificate_file('./certs/cert-ohad.pem')

port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = SSL.Connection(context, s)
s.bind(('', port))
s.listen(5)

servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print "Listening"

(connection, address) = s.accept()

print "Connection accepted"

preamble = connection.recv(util.PREAMBLE_LEN)
if(preamble != util.PREAMBLE):
    print "Premable not recognized"
    connection.send(util.ERR_CODE)
    s.close()
    sys.exit()

urlLen = int(connection.recv(util.URL_LEN))

if(urlLen == 0):
    print "Nothing to read"
    connection.send(util.ERR_CODE)
    s.close()
    sys.exit()

reqUrl = connection.recv(urlLen)

requestLen = int(connection.recv(util.REQ_LEN))

if(requestLen == 0):
    print "Nothing to read"
    connection.send(util.ERR_CODE)
    s.close()
    sys.exit()

request = connection.recv(requestLen)

url = util.split_url(reqUrl)

print "Requesting "+reqUrl
print "Sending request "+request

# now actually send the request
servSocket.connect((url[0],80))
servSocket.send(request)

# really inefficient way of reading in all the response headers
resp_hdrs = ''
content_len = ''
while('Connection: close' not in resp_hdrs):
    resp_hdrs = resp_hdrs+servSocket.recv(1)
    
    # get the content length from the header once we've read it in. super inefficient
    if('Content-Length: ' in resp_hdrs):
        # this loop will only be called once
        while('\n' not in content_len):
            content_len = content_len+servSocket.recv(1)

#read in the newline from the last header line and the empty line (\n\r\n)
# this line is needed so the server really only sends the body of the web page
servSocket.recv(4)

print resp_hdrs
# the status is in the first line of the headers, don't care about the other headers
resp_status = (resp_hdrs.split('\n'))[0]

# currently only handle good responses, can change this to handle other response codes later
if("HTTP/1.1 200 OK" not in resp_status):
    print "The web server returned this status: "+resp_status
    connection.send(util.ERR_CODE)
    servSocket.close()
    s.close()
    sys.exit()

#print content_len

bodyLen = int(content_len.rstrip('\n'))

respBody = servSocket.recv(bodyLen)

#print repr(respBody)

servSocket.close()

bodyLen = util.pad_length(bodyLen,True)

print "Sending back my response"
connection.send(util.SUCCESS_CODE)
connection.send(bodyLen)
connection.send(respBody)

s.close()
