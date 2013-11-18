import httplib
import sys
import util
import socket
import ssl

# Display info about certs
#print repr(sslSocket.server())
#print repr(sslSocket.issuer())

rawUrl = sys.argv[1]
url = util.split_url(rawUrl)
host = url[0]
path = url[1]

myConn = httplib.HTTPConnection(host)
myConn.request("GET", path)
myResp = myConn.getresponse()
myRespBody = myResp.read()
myRespBodyLen = len(myRespBody)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 12345))
sslSocket = ssl.wrap_socket(s)

urlLen = util.pad_length(len(rawUrl))

sslSocket.send(util.PREAMBLE)
sslSocket.send(urlLen)
sslSocket.send(rawUrl)

respCode = sslSocket.recv(util.RESP_CODE_LEN)
peerResp = ""

if(respCode == util.ERR_CODE):
    print "Some error occurred. Exiting."
    sys.exit()
elif(respCode == util.SUCCESS_CODE):
    print "Receiving response from trusted peer."

    bodyLen = int(sslSocket.recv(util.RESP_BODY_LEN))

    if(bodyLen == 0):
        print "Nothing to receive"
        s.close()
        sys.exit()

    peerRespBody =  sslSocket.recv(bodyLen)
    s.close()

    peerRespBodyLen = len(peerRespBody)
        
    if(myRespBodyLen != peerRespBodyLen):
        print "Responses are not of the same length."
        print "My response body length: %d" % myRespBodyLen
        print "Peer's response body length: %d " % peerRespBodyLen

    myRespBodyArr = myRespBody.splitlines()
    peerRespBodyArr = peerRespBody.splitlines()     
    
#Compare both responses up to the end of the shortest response
    areIdentical = True
    for line in range (0, min(len(myRespBodyArr),len(peerRespBodyArr))):
        if myRespBodyArr[line] != peerRespBodyArr[line]:
            areIdentical = False
            print "Responses do not match at line %d." % line
            #print myRespBodyArr[line]
            #print peerRespBodyArr[line]
        
    if(areIdentical == True):
        print "Looks good. Both responses are identical."
else:
    print "Unexpected server response code: "+respCode
  
