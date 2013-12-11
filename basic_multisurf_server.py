#Usage: python basic_multisurf_server.py <port>

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

while(1):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s = SSL.Connection(context, s)
        s.bind(('', port))
        s.listen(5)

        servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

        requestLen = int(connection.recv(util.REQ_LEN))

        if(requestLen == 0):
                print "Nothing to read"
                connection.send(util.ERR_CODE)
                s.close()
                sys.exit()

        request = connection.recv(requestLen)

        url = util.split_url(reqUrl)

        print "Requesting "+reqUrl
        #print "Sending request "+request

        # now actually send the request
        servSocket.connect((url[0],80))
        servSocket.send(request)

        # read in the response status first and then proceed accordingly
        resp_status = ''
        content_len = ''
        while('\n' not in resp_status):
                resp_status = resp_status+servSocket.recv(1)

# the status is in the first line of the headers, don't care about the other headers
        if("200 OK" in resp_status):
              #print content_len
                     
                resp_hdrs = ''
                while('<' not in resp_hdrs):
                        resp_hdrs = resp_hdrs+servSocket.recv(1)
        # get the content length from the header once we've read it in. super inefficient
                        if('Content-Length: ' in resp_hdrs):
        # this loop will only be called once
                                while('\n' not in content_len):
                                        content_len = content_len+servSocket.recv(1)

         # simply read until we reach the very first tag
        # really inefficient way of reading in all the response headers 
                print resp_hdrs
                
                respBody = ''
                bodyLen = 0
                # if content length is still '' we know that response is chunked
                # so find the chunk length before each chunk
                if(content_len == ''):
                        # this is for the first chunk
                        '''
                        size_str = ''
                        chunk_size = 65535
                        
                        first_chunk = True
                        resp_hdr_lines = resp_hdrs.splitlines()
                        size_idx = len(resp_hdr_lines)-2
                        chunk_size = int(resp_hdr_lines[size_idx].rstrip())

                        while(chunk_size > 0):
                                if(first_chunk == False):
                                        while('\n' not in size_str):
                                                size_str = size_str + servSocket.recv(1)
                                                print size_str
                                                chunk_size = int(size_str.rstrip())
                       
                        first_chunk = False '''
                        # give it some number for now
                        chunk_size = 8000
                                                
                        msg = ''
                        while('</html>' not in msg or '</HTML>' not in msg):
                                msg = servSocket.recv(chunk_size)

                                if('</html>' in msg or '</HTML>' in msg):
                                        break

                        # if we see this in our message, we know we've reached the end
                                # because it turns out that this is read in as part of the last chunk
                                '''
                                if('\r\n0\r\n\r\n' in msg):
                                        msg = msg.rstrip('\r\n0\r\n\r\n')
                                        respBody = respBody + msg
                                        break
                                print repr(msg)    
                                '''
                                respBody = respBody + msg

                        bodyLen = len(respBody)+1
                else:
                        bodyLen = int(content_len.rstrip('\n'))

                        while(len(respBody) < bodyLen-1):
                                respBody = respBody + servSocket.recv(1)

        #Now add back the '<' from before
                respBody = '<' + respBody
              
                servSocket.close()
              
                bodyLen = util.pad_length(bodyLen,True)
                
                connection.send(util.SUCCESS_CODE)
                connection.send(bodyLen)
                connection.send(respBody)
                
                s.close()
        else:
                print "The web server returned this status: "+resp_status
                connection.send(util.ERR_CODE)
                servSocket.close()
                s.close()
