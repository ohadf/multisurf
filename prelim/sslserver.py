import socket
from OpenSSL import SSL
import OpenSSL

context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('./certs/key-ohad.pem')
context.use_certificate_file('./certs/cert-ohad.pem')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = SSL.Connection(context, s)
s.bind(('', 12345))
s.listen(5)

(connection, address) = s.accept()
while True:
  try:
    data = connection.recv(65535)
  except:
    #print '[-] socket was closed abruptly'
    break
  print repr(data)
