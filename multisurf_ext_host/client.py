import httplib
import sys
import util
import socket
import ssl
import comparisons

# Display info about certs
#print repr(sslSocket.server())
#print repr(sslSocket.issuer())

class MultiSurfClient(object):
        
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.sslSocket = None
        self.requestLen = 0
        self.url = ''
        self.headers = ''
        self.myRespBody = ''
        self.myRespBodyArr = [] #this holds each line of my response body
        self.peerRespBodyArr = [] #this holds the response body for each peer
        self.myRespStatus = -1
        self.peerStatus = -1

    '''Utility functions used to communicate data between the native client and myself'''
    # hdr_list is a list of name-to-value mappings for each request header
    def parseReqHeaders(self, hdr_list):
        hdrs = ''
        for pair in hdr_list:
            hdrs = hdrs + pair['name'] + ': ' + pair['value'] + '\n'
        self.headers = hdrs
        self.requestLen = util.pad_length(len(self.headers))

    def setMyRespBody(self, resp_body):
        self.myRespBody = resp_body
        self.myRespBodyArr = resp_body.splitlines()

    def setMyStatusCode(self, status):
        self.myRespStatus = status

    def getCurUrl(self):
        return self.url
        
    '''Peer request helper functions'''
    def sendPeerReq(self,ip, port, rawUrl):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))
        self.sslSocket = ssl.wrap_socket(self.s)
        urlLen = util.pad_length(len(rawUrl))                
        self.sslSocket.send(util.PREAMBLE)
        self.sslSocket.send(urlLen)
        self.sslSocket.send(rawUrl)
        self.sslSocket.send(self.requestLen)
        self.sslSocket.send(self.headers)        
        respCode = self.sslSocket.recv(util.RESP_CODE_LEN)
        return respCode
    
    def getPeerResp(self,code):
        if(code == util.SUCCESS_CODE):
            #print "Receiving response from trusted peer."            
            bodyLen = int(self.sslSocket.recv(util.RESP_BODY_LEN))
            
            if(bodyLen == 0):
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
     
    '''Comparison helper functions'''
    #Compare both responses up to the end of the shortest response
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

    '''Multisurf protocol with peers'''
    def doProtocol(self,url):
        PEER_FILE_PATH = '/etc/opt/chrome/native-messaging-hosts/peers.txt'
        self.peerRespBodyArr = [] # reset this every time we start the protocol

        rawUrl = util.get_raw(url)
        self.url = rawUrl

        trustedPeers = []
        ports = []
        
        f = open(PEER_FILE_PATH, 'r')
        for x in range(0, util.NUM_PEERS):
            peer = f.readline().rstrip()
            port = f.readline().rstrip()
            trustedPeers.append(peer)
            ports.append(int(port))

        f.close()

        for i in range (0, len(trustedPeers)):
            # send the request to all my peers
            respCode = self.sendPeerReq(trustedPeers[i], ports[i], rawUrl)
            if (respCode == util.COMM_ERR_CODE):
                return util.COMM_ERR
            elif(respCode == util.HTTPS_REDIR_CODE):
                return util.HTTPS_ERR
        
        # respCode should be success code or unsupported code  at this point
            peerRespBody = self.getPeerResp(respCode)
                
            if(peerRespBody != None):
                self.peerRespBodyArr.append(peerRespBody)
            else:
                self.peerRespBodyArr.append(None)

        return util.GOT_BODY

    '''Response body comparison'''
    def doComparison(self):
        i = 0
        for peerRespBody in self.peerRespBodyArr:
            if(peerRespBody != None):

                path = '/tmp/peer-'+str(i)+'-'+self.url+'.txt'            
                f = open(path, 'w')
                i = i +1        
                f.write(peerRespBody)
                f.close()
                peerRespBodyLines = peerRespBody.splitlines()
                
                areIdentical = self.compareScripts(peerRespBody)
                if areIdentical:
                    continue           
                else:
                    return util.UNSAFE
            else:      
                if(self.myRespStatus != self.peerStatus):
                    #print "peer got different response. peer status: %d" % self.peerStatus
                    return util.DIFF_RESP_ERR
                else:
                    #print "peer got identical response. peer status: %d" % self.peerStatus
                    continue

        # should only get here is all peer response bodies were safe
        return util.SAFE
