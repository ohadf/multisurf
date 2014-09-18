# crawl to gather data about our requests vs peer requests to help with learning algorithm

# usage: (1) python basic_multisurf_peer.py 12345
#        (2) python collect.py <crawl_id> <time interval between requests in seconds> <# of sites visited>

import sys
import csv
from threading import Thread
import datetime
from time import sleep
import basic_multisurf_client

######## Helper functions ########

# get 100 sites from alexa top sites
def get_sites(n):
    alexa_sites = []
    with open('top-1m.csv', 'rb') as f:
        reader = csv.reader(f)
        r = list(reader)
        for item in r:
            # change to 501 for Alexa 500
            if item[0] == n:
                break
            else:
                alexa_sites.append("www."+item[1])
    return alexa_sites

# x: url, c_id: crawl_id, th_id: thread_id
def make_req(x, c_id, t, th_id):
    crawl_id = c_id
    timestamp = datetime.datetime.utcnow()
    thread_id = th_id
    url = x
    result = basic_multisurf_client.doCrawl(x, 'localhost', 12346)
    if result == 0:
        print "Something is wrong.  Don't include in database"
    else:
        request = result[2]
        response_body = result[0]
        peer_body = result[1]
    # TODO: add stuff to DB

######## Start script ########

sites = get_sites(sys.argv[4])

# starts a new thread for each site
count = 1
for s in sites:
    print s
    t = Thread(target=make_req, args=(s, sys.argv[1], count, ))
    t.start()
    count += 1
    sleep(float(sys.argv[2]))
