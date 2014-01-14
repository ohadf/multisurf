import sys
import basic_multisurf_client
import csv
import os
import util
import comparisons
from random import randrange

# run python basic_multisurf_server.py 12345 in separate shell first
# then run python crawl.py in a different shell window

def simplecrawl():
    result = basic_multisurf_client.doCrawl('www.google.com', 'localhost', 12345, 3)

def crawl():

    alexa_sites = []
    with open('top-1m.csv', 'rb') as f:
        reader = csv.reader(f)
        r = list(reader)
        for item in r:
            # change to 501 for Alexa 500
            if item[0] == '101':
                break
            else:
                alexa_sites.append("www."+item[1])

    safe = 0
    unsafe = 0
    errors = 0
    https = 0
    identical_resp = 0
    diff_resp = 0
    #print len(alexa_sites)
    for s in alexa_sites:
        if s != "www.hao123.com" or s != "www.sohu.com":
            #print "starting client for: "+s
            # 0 - number of scripts; 1 - line by line; 2 - links; 3 - two peers; 4 - combination of comparisons;
            result = basic_multisurf_client.doCrawl(s, 'localhost', 12345, 3)
            #print "finishing client for: "+s
            if result == util.SAFE:
                #print s+" : safe"
                safe += 1
            elif result == util.UNSAFE:
                #print s+" : unsafe"
                unsafe += 1
            elif result == util.HTTPS_ERR:
                #print s+": https-only"
                https +=1
            elif result == util.DIFF_RESP_ERR:
                #print s+" :different responses"
                diff_resp +=1
            elif result == util.IDENTICAL_RESP:
                #print s+" identical responses"
                identical_resp += 1
            elif result == util.COMM_ERR or result == util.INVALID_URL_ERR:
                #print s+" :error"
                errors +=1 
    return [safe,unsafe,identical_resp,diff_resp,https,errors]

#simplecrawl()
total_a = 0
total_b = 0
total_c = 0
total_d = 0
total_e = 0
total_f = 0
[a,b,c,d,e,f] = crawl()
fi = open(sys.argv[1],'w')
fi.write("The number of sites determined to be safe: "+str(a)+"\n")
fi.write("The number of sites determined to be unsafe (there is a diff): "+str(b)+"\n")
fi.write("The number of sites determined to give identical responses but no content to compare: "+str(c)+"\n")
fi.write("The number of sites determined to give different responses but no content: "+str(d)+"\n")
fi.write("The number of sites determined to be HTTPS-only: "+str(e)+"\n")
fi.write("The number of sites that gave an error: "+str(f)+"\n")
fi.write("****************************************************************************************************\n")
print "The number of sites determined to be safe: "+str(a)
print "The number of sites determined to be unsafe (there is a diff): "+str(b)
print "The number of sites determined to give identical responses but no content to compare: "+str(c)
print "The number of sites determined to give different responses but no content: "+str(d)
print "The number of sites determined to be HTTPS-only: "+str(e)
print "The number of sites that gave an error: "+str(f)
fi.close()
