import httplib
import sys
import util
import peerlib
import socket
import ssl
import parser
import comparisons

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
        self.responseType = -1


    def main(self,url=None,peer=None,port=None):
        if(self.isCrawl):
            result = self.doMyRequest(url)
            if(result == util.PEER_ERR):
                self.responseType = util.PEER_ERR
            elif(result == util.HTTPS_ERR):
                self.responseType = util.HTTPS_ERR
            else:
                myRespBody = result
                self.myRespBodyLen = len(myRespBody)
                self.myRespBodyArr = myRespBody.splitlines()
            return self.doProtocol(peer,port,url,1)
        else:
            if(len(sys.argv) < (2 + util.NUM_PEERS*2)):
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
            result = self.doMyRequest(rawUrl)
                
            if(result == util.PEER_ERR):
                return util.PEER_ERR
            elif(result == util.HTTPS_ERR):
                self.responseType = util.HTTPS_ERR
            else:
                myRespBody = result
                #print myRespBody
                self.myRespBodyLen = len(myRespBody)
                self.myRespBodyArr = myRespBody.splitlines()

#to support parser.py
#respBodies = []
#respBodies.append(myRespBody)
            portnum = 0
            for peer in trustedPeers:
                # send the request to all my peers
                self.doProtocol(peer, ports[portnum], rawUrl,portnum+1)              
        return None
                
    def sendRequest(self,rawUrl):
        url = util.split_url(rawUrl)
        host = url[0]
        path = url[1]
        self.request = self.setHeaders(host) #
        self.requestLen = util.pad_length(len(self.request))
        myConn = httplib.HTTPConnection(host)
        '''
        myConn.putrequest("GET", path)
        myConn.putheader('User-Agent', util.user_agent_hdr)
        myConn.putheader('Accept', util.accept_hdr)
        myConn.putheader('Accept-Language', util.accept_lang_hdr)
        myConn.putheader('Cookie', util.cookie_hdr)
        myConn.putheader('Connection', util.conn_hdr)
        myConn.endheaders()
        '''
        myConn.request("GET", path, "", peerlib.parseHeaders(self.request))
        myResp = myConn.getresponse()
        return myResp

    def processWebserverResponse(self,resp):
        print resp.status, resp.reason
    # see http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
        if (resp.status == 200 or "40" in str(resp.status) or "41" in str(resp.status) or 
            "50" in str(resp.status)):
            # all of these responses will have a body
            return util.RESP_HASBODY
        elif ("30" in str(resp.status)):
            # it's a redirect, so check if we can get the new location via HTTP
            newUri = resp.getheader("Location")        
            if("https://" in newUri):
                return util.RESP_REDIR_HTTPS
            elif("http://" in newUri):
                return util.RESP_REDIR_GOOD
            else:
                # Location header was empty
                return util.RESP_REDIR_NOLOC
        else:
            #print "web server returned this status: %d " % resp.status
            return None

    def processRespType(self,respType,resp):
        if(respType == util.RESP_HASBODY):
            return resp.read()
        elif(respType == util.RESP_REDIR_HTTPS):
            return respType
        elif(respType == util.RESP_REDIR_NOLOC):
            return respType
        elif(respType == util.RESP_REDIR_GOOD):            
            newRaw = resp.getheader("Location").strip().split("//")[1]
            serverResp = self.sendRequest(newRaw)
            #print "first redirect"
            respType1 = self.processWebserverResponse(serverResp)
            if(respType1 == util.RESP_HASBODY):
                return serverResp.read()
            else:
                #print "web server tried a second redirect"
                return respType1
        else:
            #print "web server responded with an unsupported code"
            return None
        
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
        if(code == util.SUCCESS_CODE):
            #print "Receiving response from trusted peer."
            
            bodyLen = int(self.sslSocket.recv(util.RESP_BODY_LEN))
            
            if(bodyLen == 0):
                print "Nothing to receive"
                self.s.close()
                return None
            
            peerRespBody = self.sslSocket.recv(bodyLen)
            self.s.close()
            return peerRespBody
        return None

    def processPeerResp(self,resp):
        peerRespBodyLen = len(resp)
        
        if(self.myRespBodyLen != peerRespBodyLen):
            '''
            print "Responses are not of the same length."
            print "My response body length: %d" % self.myRespBodyLen
            print "Peer's response body length: %d " % peerRespBodyLen
            '''
        return resp.splitlines()  
                
#Compare both responses up to the end of the shortest response
    def compareByLine(self,peerArr):
        areIdentical = True
        for line in range (0, min(len(self.myRespBodyArr),len(peerArr))):
            if self.myRespBodyArr[line] != peerArr[line]:
                areIdentical = False
                #print "Responses do not match at line %d." % line
                #print "conflict: %r \n %r" % (self.myRespBodyArr[line], peerArr[line])
                break
        return areIdentical

    def compareDiff(self,peerArr):
        areIdentical = True
        if (comparisons.is_diff(self.myRespBodyArr, peerArr)) == True:
            areIdentical = False
            f = open('diff_results.txt', 'a')
            diff = (comparisons.print_diff(self.myRespBodyArr, peerArr))[1]
        return areIdentical

    def setHeaders(self, host):
        host_hdr = 'Host: %s\n' % host
        user_agent_hdr = 'User-Agent: '+util.user_agent_hdr+'\n'
        accept_hdr = 'Accept: '+util.accept_hdr+'\n'
        accept_lang_hdr = 'Accept-Language: '+util.accept_lang_hdr+'\n'
        cookie_hdr = 'Cookie: '+util.cookie_hdr+'\n'
        conn_hdr = 'Connection: '+util.conn_hdr+'\n'
        return host_hdr+user_agent_hdr+accept_hdr+accept_lang_hdr+cookie_hdr+conn_hdr
                                        
    def doMyRequest(self,rawUrl):
        serverResp = self.sendRequest(rawUrl)
        respType = self.processWebserverResponse(serverResp)
        result = self.processRespType(respType,serverResp)

        if(result == util.RESP_REDIR_HTTPS):
            #print "web server is redirecting to HTTPS"
            return util.HTTPS_ERR
        elif(result == None or result == util.RESP_REDIR_NOLOC or result == util.RESP_REDIR_GOOD):
            #print "no good: "+result
            return util.PEER_ERR
        else:
            #print "this should be good: "+result
            return result

# Protocol starts here
    def doProtocol(self,peer,port,url,peerID):
        respCode = self.sendPeerReq(peer, port, url)
        if (respCode == util.ERR_CODE):
            #print "Peer responded with an error."
            return util.PEER_ERR
        elif(respCode == util.HTTPS_REDIR_CODE):
            #print "Peer trying to redirect to HTTPS"
            if(self.responseType == util.HTTPS_ERR):
                return util.IDENTICAL
            else:
                return util.HTTPS_ERR
        
        # respCode should be success code at this point
        peerRespBody = self.getPeerResp(respCode)
                #print peerRespBody
                
        if(peerRespBody != None):
            peerRespBodyArr = self.processPeerResp(peerRespBody)
            
            areIdentical = self.compareDiff(peerRespBodyArr)
            #areIdentical = self.compareByLine(peerRespBodyArr)
            if areIdentical:
                #print "Looks good for peer %d. Both responses are identical." % (peerID)
                return util.IDENTICAL
            
            else:
                return util.NOT_IDENTICAL_ERR  
        
def doCrawl(url,peer,port):
    #print 'Entry point'
    client = MultiSurfClient(True)
    #print 'created client'
    result = client.main(url,peer,port)
    #print 'got result'
    return result

if  __name__ == "__main__":
        client = MultiSurfClient(False)
        client.main()
