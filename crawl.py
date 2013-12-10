import sys
import basic_multisurf_client
import csv
import os

def simplecrawl():
    result = basic_multisurf_client.doCrawl('www.google.com', 'localhost', 12345)

def crawl():

    alexa_sites = []
    with open('top-1m.csv', 'rb') as f:
        reader = csv.reader(f)
        r = list(reader)
        for item in r:
            if item[0] == 2:
                break
            else:
                alexa_sites.append("www."+item[1])

    safe = 0
    unsafe = 0
    errors = 0
    for s in alexa_sites:
        result = basic_multisurf_client.doCrawl(s, 'localhost', 12345)
        if result == True:
            safe += 1
        elif result == False:
            unsafe += 1
        else:
            errors += 1    
    return [safe,unsafe,unknown]


simplecrawl()
#[a,b,c] = crawl()
#print "The number of sites determined to be safe: "+str(a)
#print "The number of sites determined to be unsafe (there is a diff): "+str(b)
#print "The number of sites that gave an error: "+str(c)
