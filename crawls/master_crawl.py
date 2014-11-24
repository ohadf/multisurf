# script to do a number of crawls using collect.py

import os
import threading
import time
import sys

def start_peer(x):
    os.system("python basic_multisurf_peer.py "+str(x))

def start_crawl(a,b,c,d):
    os.system("python collect.py "+str(a)+" "+str(b)+" "+str(c)+" "+user+" "+pwd)

p = 12345
crawl_id = 1

user = sys.argv[1]
pwd = sys.argv[2]

# crawl 1: one peer on local machine, 1 second between requests, 100 sites (format of args: <crawl_id> <time interval between requests in seconds> <# of sites visited> <# of peers>)
thread = threading.Thread(target=start_peer, args=(p,))
thread.start()
print "Started peer..."
time.sleep(5)
thread = threading.Thread(target=start_crawl, args=(crawl_id, 1, 10, 1))
thread.start()
print "Started client..."

# crawl 2: one peer on local machine, 60 seconds between requests, 100 sites (format of args: <crawl_id> <time interval between requests in seconds> <# of sites visited> <# of peers>)
#crawl_id += 1
#thread = threading.Thread(target=start_crawl, args=(crawl_id, 60, 100, 1))
#thread.start()

# crawl 3: one peer on local machine, 300 seconds between requests, 100 sites (format of args: <crawl_id> <time interval between requests in seconds> <# of sites visited> <# of peers>)
#crawl_id += 1
#thread = threading.Thread(target=start_crawl, args=(crawl_id, 300, 100, 1))
#thread.start()

# crawl 4: two peers on local machine, 1 second between requests, 100 sites (format of args: <crawl_id> <time interval between requests in seconds> <# of sites visited> <# of peers>)
#p2 = p + 1
#thread = threading.Thread(target=start_peer, args=(p2,))
#thread.start()
#thread = threading.Thread(target=start_crawl, args=(crawl_id, 1, 100, 2))
#thread.start()

# crawl 5: two peers on local machine, 60 seconds between requests, 100 sites (format of args: <crawl_id> <time interval between requests in seconds> <# of sites visited> <# of peers>)
#crawl_id += 1
#thread = threading.Thread(target=start_crawl, args=(crawl_id, 60, 100, 2))
#thread.start()

# crawl 6: two peers on local machine, 300 seconds between requests, 100 sites (format of args: <crawl_id> <time interval between requests in seconds> <# of sites visited> <# of peers>)
#crawl_id += 1
#thread = threading.Thread(target=start_crawl, args=(crawl_id, 300, 100, 2))
#thread.start()
