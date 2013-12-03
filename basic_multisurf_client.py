#Usage: python basic_multisurf_client.py <url> <peer1> <peer1 port> <peer2> <peer2 port>

import httplib
import sys
import util
import socket
import ssl

# Display info about certs
#print repr(sslSocket.server())
#print repr(sslSocket.issuer())

def sendRequest(h, p):
	myConn = httplib.HTTPConnection(h)
	myConn.request("GET", p)
	myResp = myConn.getresponse()
	return myResp.read()
  

def sendPeerReq(ip, port, rawUrl):
	global s
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, port))
	global sslSocket 
	sslSocket = ssl.wrap_socket(s)

	urlLen = util.pad_length(len(rawUrl))

	sslSocket.send(util.PREAMBLE)
	sslSocket.send(urlLen)
	sslSocket.send(rawUrl)

	respCode = sslSocket.recv(util.RESP_CODE_LEN)
	return respCode

def getPeerResp(code):
	if(code == util.ERR_CODE):
    		print "Some error occurred. Exiting."
		return None
	elif(code == util.SUCCESS_CODE):
		print "Receiving response from trusted peer."
	
		global s
		global sslSocket
    		bodyLen = int(sslSocket.recv(util.RESP_BODY_LEN))

    		if(bodyLen == 0):
       			print "Nothing to receive"
        		s.close()
        		return None

    		peerRespBody = sslSocket.recv(bodyLen)
    		s.close()
		return peerRespBody

def processPeerResp(resp):
	peerRespBodyLen = len(resp)
        
    	if(myRespBodyLen != peerRespBodyLen):
        	print "Responses are not of the same length."
       		print "My response body length: %d" % myRespBodyLen
        	print "Peer's response body length: %d " % peerRespBodyLen

    	
  	return peerRespBody.splitlines()  

#Compare both responses up to the end of the shortest response
def compareByLine(myArr, peerArr):
	areIdentical = True
    	for line in range (0, min(len(myArr),len(peerArr))):
        	if myArr[line] != peerArr[line]:
            		areIdentical = False
            		print "Responses do not match at line %d." % line
	return areIdentical


# Protocol starts here

if len(sys.argv) < 6:
	print "Usage: python basic_multisurf_client.py <url> <peer1> <peer1 port> <peer2> <peer2 port>"
	sys.exit();

rawUrl = sys.argv[1]
url = util.split_url(rawUrl)
host = url[0]
path = url[1]

trustedPeers = []
trustedPeers.append(sys.argv[2])
trustedPeers.append(sys.argv[4])

ports = []
ports.append(int(sys.argv[3]))
ports.append(int(sys.argv[5]))

# send my request to the server
myRespBody = sendRequest(host,path)
myRespBodyLen = len(myRespBody)
myRespBodyArr = myRespBody.splitlines()

# just to initialize, but this is done for each trusted peer, too
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sslSocket = None

portnum = 0
for peer in trustedPeers:
	# send the request to all my peers
	respCode = sendPeerReq(peer, ports[portnum], rawUrl)
	peerRespBody = getPeerResp(respCode)

	if(peerRespBody != None):
		peerRespBodyArr = processPeerResp(peerRespBody)

		if(compareByLine(myRespBodyArr, peerRespBodyArr)):
        		print "Looks good for peer %d. Both responses are identical." % (portnum+1)
		else:
    			print "Unexpected server response code: "+respCode  


	portnum = portnum + 1
	
  
