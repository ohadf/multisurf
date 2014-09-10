import urllib2

def get_data(u):
    req = urllib2.Request('http://www.google.com')
    print req
    #f = urllib2.urlopen(req)
    #print f.read()

get_data(1)
