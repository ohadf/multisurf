#Usage: python basic_multisurf_server.py <port>

import httplib
import socket
import collections
from OpenSSL import SSL
import OpenSSL
import util
import peerlib
import sys

context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('../certs/key-ohad.pem')
context.use_certificate_file('../certs/cert-ohad.pem')

port = int(sys.argv[1])

while(1):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s = SSL.Connection(context, s)
    s.bind(('', port))
    s.listen(5)
    
    servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #print "Listening"
    
    (connection, address) = s.accept()
    
    #print "Connection accepted"
    
    preamble = connection.recv(util.PREAMBLE_LEN)
    if(preamble != util.PREAMBLE):
        print "Premable not recognized"
        connection.send(util.COMM_ERR_CODE)
        s.close()
        sys.exit()
        
    urlLen = int(connection.recv(util.URL_LEN))
        
    if(urlLen == 0):
        print "Nothing to read"
        connection.send(util.COMM_ERR_CODE)
        s.close()
        sys.exit()

    reqUrl = connection.recv(urlLen)

    requestLen = int(connection.recv(util.REQ_LEN))

    if(requestLen == 0):
        print "Nothing to read"
        connection.send(util.COMM_ERR_CODE)
        s.close()
        sys.exit()

    request = connection.recv(requestLen)

    headers = peerlib.parseHeaders(request)
    
    # TODO: change this to urlib header dict
    print "Requesting "+reqUrl
    #print "Sending request "+request

        # now actually send the request

    resp = peerlib.sendRequest(reqUrl,headers)

    (respType,status) = peerlib.processWebserverResponse(resp)

    (result,status1) = peerlib.processRespType(respType,resp,headers)

    if(result == util.RESP_REDIR_HTTPS):
        connection.send(util.HTTPS_REDIR_CODE)
    elif(result == util.RESP_UNSUPP or result == util.RESP_REDIR_GOOD):
        connection.send(util.UNSUPP_CODE)
        if(result == util.RESP_UNSUPP):
            #print "got here unsupp: %d " % status
            connection.send(str(status))
        else:
            #print "got here: %d " % status1
            connection.send(str(status1))
    else:
        respBody = result
        #print respBody
        bodyLen = util.pad_length(len(respBody),True)
        #print bodyLen
        print "Sending back my response"
        connection.send(util.SUCCESS_CODE)
        connection.send(bodyLen)

        if(int(bodyLen) > 0):
            connection.send(respBody)
        else:
            connection.send(str(status))
        
    s.close()
