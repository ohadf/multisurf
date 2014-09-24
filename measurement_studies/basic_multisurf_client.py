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

#modify line 272 to change comparison technique

class MultiSurfClient(object):
        
    def __init__(self, crawling, testingLatency, comparison):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.sslSocket = None
        self.requestLen = 0
        self.request = ''
        self.myRespBody = ''
        self.myRespBodyLen = 0
        self.myRespBodyArr = []
        self.isCrawl = crawling
        self.myRespStatus = -1
        self.peerStatus = -1
        self.isLatency = testingLatency
        self.comp = comparison

    def main(self,url=None,peer=None,port=None,peerNum=None):
        if(self.isLatency):
            result = self.doMyRequest(url)
            return result
        elif(self.isCrawl):
            result = self.doMyRequest(url)
            my_req = self.request
            if(result == util.INVALID_URL_ERR or result == util.HTTPS_ERR):
                return result
            elif(result != util.RESP_UNSUPP):
                self.myRespBody = result
                self.myRespBodyLen = len(self.myRespBody)
                self.myRespBodyArr = self.myRespBody.splitlines()
                peerBodyList = []
                for x in range(0,peerNum):
                    peerBody = self.doProtocol(peer,port+x,url,1)
                    peerBodyList.append(peerBody)
                return [self.myRespBody, my_req]+peerBodyList
            return 0
            #if self.comp == 3:
            #    return self.doProtocol2(peer,port,url,1,peer,port,url,2)
            #else:
            #    return self.doProtocol(peer,port,url,1)
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
                
            if(result != util.INVALID_URL_ERR and result != util.HTTPS_ERR):
                if(result != util.RESP_UNSUPP):
                    myRespBody = result
                #print myRespBody
                    self.myRespBodyLen = len(myRespBody)
                    self.myRespBodyArr = myRespBody.splitlines()
            else:
                return None
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
        try:
            myConn.request("GET", path, "", peerlib.parseHeaders(self.request))
            myResp = myConn.getresponse()
            return myResp
        except socket.gaierror:
            return util.INVALID_URL_ERR
        except socket.error:
            return util.INVALID_URL_ERR

    def processWebserverResponse(self,resp):
    # see http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html        
        if(resp == util.INVALID_URL_ERR):
            return util.INVALID_URL_ERR

        #print resp.status, resp.reason
        self.myRespStatus = resp.status

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
                return util.RESP_UNSUPP
        else:
            #print "web server returned this status: %d " % resp.status
            return util.RESP_UNSUPP

    def processRespType(self,respType,resp):
        if(respType == util.INVALID_URL_ERR):
            return respType

        if(respType == util.RESP_HASBODY):
            return resp.read()
        elif(respType == util.RESP_REDIR_HTTPS or respType == util.RESP_UNSUPP):
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
                #print "No body"
                self.peerStatus = int(self.sslSocket.recv(util.STATUS_LEN))
                return None
            peerRespBody = self.sslSocket.recv(bodyLen)
            self.s.close()
            return peerRespBody
        elif(code == util.UNSUPP_CODE):
            self.peerStatus = int(self.sslSocket.recv(util.STATUS_LEN))
            return None
        self.s.close()
        return None

    def processPeerResp(self,resp):
        peerRespBodyLen = len(resp)
        
        if(self.myRespBodyLen != peerRespBodyLen):
            '''
            print "Responses are not of the same length."
            print "My response body length: %d" % self.myRespBodyLen
            print "Peer's response body length: %d " % peerRespBodyLen
            '''
        return resp  
                
#Compare both responses up to the end of the shortest response
    #def compareByLine(self,peerArr):
    #    areIdentical = True
    #    for line in range (0, min(len(self.myRespBodyArr),len(peerArr))):
    #       if self.myRespBodyArr[line] != peerArr[line]:
    #            areIdentical = False
    #            #print "Responses do not match at line %d." % line
    #            #print "conflict: %r \n %r" % (self.myRespBodyArr[line], peerArr[line])
    #            break
    #   return areIdentical

    def compareByLine(self, peerArr):
        areIdentical = True
        areIdentical = comparisons.line_by_line(self.myRespBody, peerArr)
        return areIdentical

    def compareScripts(self,peerArr):
        areIdentical = True
        [l1,l2] = comparisons.count_scripts(self.myRespBody, peerArr)
        if l1 != l2:
            areIdentical = False
        return areIdentical

    def compareByLinks(self,peerArr):
        areIdentical = True
        [l1,l2] = comparisons.compare_links(self.myRespBody, peerArr)
        if l1 != l2:
            areIdentical = False
        return areIdentical

    def compareWithTwoPeers(self,peerArr1,peerArr2):
        areIdentical = True
        result = comparisons.compare_with_two_peers(self.myRespBody,peerArr1,peerArr2)
        if result == 1 or result == 2:
            areIdentical == False
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
        elif(result == util.RESP_UNSUPP or result == util.RESP_REDIR_GOOD):
            #print "no good: "+result
            return util.RESP_UNSUPP
        elif(result == util.INVALID_URL_ERR):
            #print "Invalid URL requested"
            return util.INVALID_URL_ERR
        else:
            #print "this should be good: "+result
            return result

# Protocol starts here
    def doProtocol(self,peer,port,url,peerID):
        try:
            respCode = self.sendPeerReq(peer, port, url)
        except Exception:
            print "EXCEPTION"
            return 0
            
        if (respCode == util.COMM_ERR_CODE):
            #print "Peer responded with an error."
            return util.COMM_ERR
        elif(respCode == util.HTTPS_REDIR_CODE):
            #print "Peer got different response"
            return util.DIFF_RESP_ERR
        
        # respCode should be success code or unsupported code  at this point
        peerRespBody = self.getPeerResp(respCode)
                #print peerRespBody
        return peerRespBody
        if(peerRespBody != None):
            peerRespBodyArr = self.processPeerResp(peerRespBody)
            
            areIdentical = False
            if self.comp == 0:
                areIdentical = self.compareScripts(peerRespBodyArr)
            elif self.comp == 1:
                areIdentical = self.compareByLine(peerRespBodyArr)
            elif self.comp == 2:
                areIdentical = self.compareByLinks(peerRespBodyArr)
            else:
                areIdentical = False
                #use all 3 algorithms for a more accurate result
                #print "implement me!"
            
            if areIdentical:
                #print "Looks good for peer %d. Both responses are identical." % (peerID)
                #print "Site is safe"
                return util.SAFE
            
            else:
                #print "Site is unsafe. My status: %s" % self.myRespStatus
                return util.UNSAFE
        else:
            if(self.myRespStatus != self.peerStatus):
                #print "peer got different response. peer status: %d" % self.peerStatus
                return util.DIFF_RESP_ERR
            else:
                #print "peer got identical response. peer status: %d" % self.peerStatus
                return util.IDENTICAL_RESP
        
# Protocol for 2 peers starts here
    def doProtocol2(self,peer,port,url,peerID,peer2,port2,url2,peerID2):
        respCode1 = self.sendPeerReq(peer, port, url)
        if (respCode1 == util.COMM_ERR_CODE):
            #print "Peer responded with an error."
            return util.COMM_ERR
        elif(respCode1 == util.HTTPS_REDIR_CODE):
            #print "Peer got different response"
            return util.DIFF_RESP_ERR

        # respCode should be success code or unsupported code  at this point
        peerRespBody1 = self.getPeerResp(respCode1)
                #print peerRespBody

        respCode2 = self.sendPeerReq(peer2, port2, url2)
        if (respCode2 == util.COMM_ERR_CODE):
            #print "Peer responded with an error."
            return util.COMM_ERR
        elif(respCode2 == util.HTTPS_REDIR_CODE):
            #print "Peer got different response"
            return util.DIFF_RESP_ERR

        # respCode should be success code or unsupported code  at this point
        peerRespBody2 = self.getPeerResp(respCode2)
                #print peerRespBody
                
        if(peerRespBody1 != None and peerRespBody2 != None):
            peerRespBodyArr1 = self.processPeerResp(peerRespBody1)
            peerRespBodyArr2 = self.processPeerResp(peerRespBody2)
            
            areIdentical = False
            if self.comp == 0:
                areIdentical = self.compareScripts(peerRespBodyArr)
            elif self.comp == 1:
                areIdentical = self.compareByLine(peerRespBodyArr)
            elif self.comp == 2:
                areIdentical = self.compareByLinks(peerRespBodyArr)
            elif self.comp == 3:
                areIdentical = self.compareWithTwoPeers(peerRespBodyArr1,peerRespBodyArr2)
            else:
                areIdentical = False
                #use all 3 algorithms for a more accurate result
                #print "implement me!"
            
            if areIdentical:
                #print "Looks good for peer %d. Both responses are identical." % (peerID)
                #print "Site is safe"
                return util.SAFE
            
            else:
                #print "Site is unsafe. My status: %s" % self.myRespStatus
                return util.UNSAFE
        else:
            if(self.myRespStatus != self.peerStatus):
                #print "peer got different response. peer status: %d" % self.peerStatus
                return util.DIFF_RESP_ERR
            else:
                #print "peer got identical response. peer status: %d" % self.peerStatus
                return util.IDENTICAL_RESP

def doCrawl(url,peer,port,numPeers):
    #print 'Entry point'
    client = MultiSurfClient(True,False,1)
    print 'created client'
    result = client.main(url,peer,port,numPeers)
    #print 'got result'
    return result

def measure_baseline_latency(url,peer,port,numPeers):
    client = MultiSurfClient(True,True,0)
    result = client.main(url,peer,port,numPeers)
    return result

def measure_multisurf_latency(url,peer,port,compAlgo,numPeers):
    client = MultiSurfClient(True,False,compAlgo)
    result = client.main(url,peer,port,numPeers)
    return result

if  __name__ == "__main__":
        client = MultiSurfClient(False, False, False)
        client.main()
