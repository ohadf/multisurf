import sys
import basic_multisurf_client
import csv
import os
import util

# run python basic_multisurf_server.py 12345 in separate shell first
# then run python crawl.py in a different shell window

def simplecrawl():
    result = basic_multisurf_client.doCrawl('www.googleusercontent.com', 'localhost', 12345)

def crawl():

    alexa_sites = []
    with open('top-1m.csv', 'rb') as f:
        reader = csv.reader(f)
        r = list(reader)
        for item in r:
            # change to 501 for Alexa 500
            if item[0] == '200':
                break
            else:
                alexa_sites.append("www."+item[1])

    safe = 0
    unsafe = 0
    errors = 0
    https = 0
    print len(alexa_sites)
    for s in alexa_sites:
        if s != 'www.akamaihd.net' and s != 'www.thepiratebay.sx' and s != 'www.t.co' and s != 'www.bp.blogspot.com' and s != 'www.media.tumblr.com' and s != 'www.secureserver.net' and s != 'www.statcounter.com':
            print "starting client for: "+s
            result = basic_multisurf_client.doCrawl(s, 'localhost', 12345)
            print "finishing client for: "+s
            if result == util.IDENTICAL:
                print s+" : safe"
                safe += 1
            elif result == util.NOT_IDENTICAL_ERR:
                print s+" : unsafe"
                unsafe += 1
            elif result == util.HTTPS_ERR:
                print s+": https"
                https +=1
            else:   
                print s+" : error"
                errors += 1    
    return [safe,unsafe,errors,https]


#simplecrawl()
[a,b,c,d] = crawl()
print "The number of sites determined to be safe: "+str(a)
print "The number of sites determined to be unsafe (there is a diff): "+str(b)
print "The number of sites determined to be HTTPS: "+str(d)
print "The number of sites that gave an error: "+str(c)
