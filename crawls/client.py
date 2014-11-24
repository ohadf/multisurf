import httplib
import util
import peerlib
import socket
import ssl

class MultiSurfClient(object):
        
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.sslSocket = None
        self.requestLen = 0
        self.request = ''
        self.myRespBody = ''
        self.myRespBodyLen = 0
        self.myRespBodyArr = []
        self.myRespStatus = -1

    def main(self,url=None,peer=None,port=None):
        result = self.doMyRequest(url)
        my_req = self.request
        if(result == util.INVALID_URL_ERR or result == util.HTTPS_ERR):
            return result
        elif(result != util.RESP_UNSUPP):
            self.myRespBody = result
            self.myRespBodyLen = len(self.myRespBody)
            self.myRespBodyArr = self.myRespBody.splitlines()
            return [self.myRespBody, my_req]
        return 0    

    def setHeaders(self, host):
        host_hdr = 'Host: %s\n' % host
        user_agent_hdr = 'User-Agent: '+util.user_agent_hdr+'\n'
        accept_hdr = 'Accept: '+util.accept_hdr+'\n'
        accept_lang_hdr = 'Accept-Language: '+util.accept_lang_hdr+'\n'
        cookie_hdr = 'Cookie: '+util.cookie_hdr+'\n'
        conn_hdr = 'Connection: '+util.conn_hdr+'\n'
        return host_hdr+user_agent_hdr+accept_hdr+accept_lang_hdr+cookie_hdr+conn_hdr     
                
    def sendRequest(self,rawUrl):
        print "Sending request: "+rawUrl
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

def doCrawl(url,peer,port):
    client = MultiSurfClient()
    result = client.main(url,peer,port)
    return result

if  __name__ == "__main__":
        client = MultiSurfClient()
        client.main()
