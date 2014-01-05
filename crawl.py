import sys
import basic_multisurf_client
import csv
import os

# run python basic_multisurf_server.py 12345 in separate shell first
# then run python crawl.py in a different shell window

def simplecrawl():
    result = basic_multisurf_client.doCrawl('www.google.com', 'localhost', 12345)

def crawl():

    alexa_sites = []
    with open('top-1m.csv', 'rU') as f:
        reader = csv.reader(f)
        r = list(reader)
        for position in range(67,501):
            # change to 501 for Alexa 500
            #if item[0] == '501':
            #    break
            #elif r.index(item) >= 36 or r.index(item) <= 501:
            alexa_sites.append("www."+r[position][1])

    safe = 0
    unsafe = 0
    errors = 0
    print len(alexa_sites)
    for s in alexa_sites:
        print "starting client for: "+s
        result = basic_multisurf_client.doCrawl(s, 'localhost', 12345)
        print "finishing client for: "+s
        print result
        if result == 2:
            print s+" : safe"
            safe += 1
        elif result == 1:
            print s+" : unsafe"
            unsafe += 1
        else:   
            print s+" : error"
            errors += 1 
        print str(safe)+" "+str(unsafe)+" "+str(errors)   
    return [safe,unsafe,errors]


#simplecrawl()
[a,b,c] = crawl()
print "The number of sites determined to be safe: "+str(a)
print "The number of sites determined to be unsafe (there is a diff): "+str(b)
print "The number of sites that gave an error: "+str(c)
