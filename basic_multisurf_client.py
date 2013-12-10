import httplib
import sys
import util
import socket
import ssl
import parser

# Display info about certs
#print repr(sslSocket.server())
#print repr(sslSocket.issuer())

class MultiSurfClient(object):
        
    def __init__(self, crawling):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.sslSocket = None
        self.requestLen = 0
        self.request = ''
        self.myRespBody = ''
        self.myRespBodyLen = 0
        self.myRespBodyArr = []
        self.isCrawl = crawling


    def main(self,url=None,peer=None,port=None):
        if(self.isCrawl):
            myRespBodyArr = self.doMyRequest(url)
            return self.doProtocol(peer,port,url,1)
        else:
            if len(sys.argv) < 2 + util.NUM_PEERS*2:
                print "Usage: python basic_multisurf_client.py <url> <peer1> <peer1 port> <peer2> <peer2 port> etc..."
                return False

            rawUrl = sys.argv[1]
            trustedPeers = []
            arg = 2
            while (arg <= 2*util.NUM_PEERS):
                trustedPeers.append(sys.argv[arg])
                arg += 2
            ports = []
            arg = 3
            while (arg <= 2*util.NUM_PEERS+1):
                ports.append(int(sys.argv[arg]))
                arg += 2
            # send my request to the server
            self.myRespBodyArr = self.doMyRequest(rawUrl)
                
#to support parser.py
#respBodies = []
#respBodies.append(myRespBody)
            portnum = 0
            for peer in trustedPeers:
                # send the request to all my peers
                print portnum
                areIdentical = self.doProtocol(peer, ports[portnum], rawUrl,portnum+1)    
            return None
                
    def sendRequest(self,h, p):
        self.request = self.setRequest(p, h) #
        self.requestLen = util.pad_length(len(self.request))
        myConn = httplib.HTTPConnection(h)
        myConn.putrequest("GET", p)
        myConn.putheader('User-Agent', util.user_agent_hdr)
        myConn.putheader('Accept', util.accept_hdr)
        myConn.putheader('Accept-Language', util.accept_lang_hdr)
        myConn.putheader('Cookie', util.cookie_hdr)
        myConn.putheader('Connection', util.conn_hdr)
        myConn.endheaders()
        myResp = myConn.getresponse()
        return myResp.read()        
        
    def sendPeerReq(self,ip, port, rawUrl):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))
        self.sslSocket = ssl.wrap_socket(self.s)
        urlLen = util.pad_length(len(rawUrl))
                
        self.sslSocket.send(util.PREAMBLE)
        self.sslSocket.send(urlLen)
        self.sslSocket.send(rawUrl)
        self.sslSocket.send(self.requestLen)
        self.sslSocket.send(self.request)
        respCode = self.sslSocket.recv(util.RESP_CODE_LEN)
        return respCode
        
    def getPeerResp(self,code):
        if(code == util.ERR_CODE):
            print "Some error occurred. Exiting."
            return None
        elif(code == util.SUCCESS_CODE):
            print "Receiving response from trusted peer."
                        
            bodyLen = int(self.sslSocket.recv(util.RESP_BODY_LEN))
                        
            if(bodyLen == 0):
                print "Nothing to receive"
                self.s.close()
                return None

            peerRespBody = self.sslSocket.recv(bodyLen)
            self.s.close()
            return peerRespBody

    def processPeerResp(self,resp):
        peerRespBodyLen = len(resp)
        
        if(self.myRespBodyLen != peerRespBodyLen):
            print "Responses are not of the same length."
            print "My response body length: %d" % self.myRespBodyLen
            print "Peer's response body length: %d " % peerRespBodyLen
        return resp.splitlines()  
                
#Compare both responses up to the end of the shortest response
    def compareByLine(self,peerArr):
        areIdentical = True
        for line in range (0, min(len(self.myRespBodyArr),len(peerArr))):
            if self.myRespBodyArr[line] != peerArr[line]:
                areIdentical = False
                print "Responses do not match at line %d." % line
                #print "conflict: %r \n %r" % (self.myRespBodyArr[line], peerArr[line])
                break
        return areIdentical

    def setRequest(self,url, host):
        req_type = 'GET %s HTTP/1.1\n' % url
        host_hdr = 'Host: %s\n' % host
        user_agent_hdr = 'User-Agent: '+util.user_agent_hdr+'\n'
        accept_hdr = 'Accept: '+util.accept_hdr+'\n'
        accept_lang_hdr = 'Accept-Language: '+util.accept_lang_hdr+'\n'
        cookie_hdr = 'Cookie: '+util.cookie_hdr+'\n'
        conn_hdr = 'Connection: '+util.conn_hdr+'\n'
        return req_type+host_hdr+user_agent_hdr+accept_hdr+accept_lang_hdr+cookie_hdr+conn_hdr+'\n'
                                        
    def doMyRequest(self,rawUrl):
        url = util.split_url(rawUrl)
        host = url[0]
        path = url[1]
        self.myRespBody = self.sendRequest(host,path)
        print 'My response'
        print self.myRespBody
        self.myRespBodyLen = len(self.myRespBody)
        return self.myRespBody.splitlines()

# Protocol starts here
    def doProtocol(self,peer,port,url,peerID):
        respCode = self.sendPeerReq(peer, port, url)
        peerRespBody = self.getPeerResp(respCode)
        print peerRespBody

    #to support parser.py
    #respBodies.append(peerRespBody)
                
        if(peerRespBody != None):
            peerRespBodyArr = self.processPeerResp(peerRespBody)
                        
            areIdentical = self.compareByLine(peerRespBodyArr)
            if areIdentical:
                print "Looks good for peer %d. Both responses are identical." % (peerID)
            return areIdentical
        return False
                        
#to support parser.py and assumes 2 trusted peers        
#parser.new_parse_and_compare(respBodies[0], respBodies[1], respBodies[2])  
        
def doCrawl(url,peer,port):
    print 'Enrty point'
    client = MultiSurfClient(True)
    print 'created client'
    result = client.main(url,peer,port)
    print 'got result'
    return result

if  __name__ == "__main__":
        client = MultiSurfClient(False)
        client.main()
