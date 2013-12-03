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

url = util.split_url(reqUrl)

print "Requesting "+reqUrl

conn = httplib.HTTPConnection(url[0])
conn.request("GET", url[1])
resp = conn.getresponse()
respBody = resp.read()

bodyLen = util.pad_length(len(respBody),True)

print "Sending back my response"
connection.send(util.SUCCESS_CODE)
connection.send(bodyLen)
connection.send(respBody)

s.close()
