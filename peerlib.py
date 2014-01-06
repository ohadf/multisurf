import httplib
import util
import collections

def parseHeaders(request):
    headers = collections.OrderedDict()
    for line in request.splitlines():
        hdr_line = line.split(":")
        header = hdr_line[0].strip()
        value = hdr_line[1].strip()
        headers[header] = value
    return headers

def sendRequest(rawUrl, hdrs):
    url = util.split_url(rawUrl)
    host = url[0]
    path = url[1]
    servConn = httplib.HTTPConnection(host)
    servConn.request("GET", path, "", hdrs)
    return servConn.getresponse()

def processWebserverResponse(resp):
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
        print "web server returned this status: %d " % resp.status
        return None

def processRespType(respType,resp,hdrs):
    if(respType == util.RESP_HASBODY):
        return resp.read()
    elif(respType == util.RESP_REDIR_HTTPS):
        return respType
    elif(respType == util.RESP_REDIR_NOLOC):
        return respType
    elif(respType == util.RESP_REDIR_GOOD):
         # redirection so get the location so we can redirect
        newRaw = resp.getheader("Location").strip().split("//")[1]
        serverResp = sendRequest(newRaw,hdrs)
        print "first redirect"
        respType1 = processWebserverResponse(serverResp)
        if(respType1 == util.RESP_HASBODY):
            return serverResp.read()
        else:
            print "server tried a second redirect"
            return respType1
    else:
        return None
