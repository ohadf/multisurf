# script to do a number of crawls using collect.py

import os
import threading

def start_peer(x):
    print "here1"
    os.system("python basic_multisurf_peer.py "+str(x))
    print "here2"

def start_crawl(a,b,c,d):
    os.system("python collect.py "+str(a)+" "+str(b)+" "+str(c)+" "+str(d))

p = 12345
crawl_id = 1

# crawl 1: one peer on local machine, 1 second between requests, 100 sites (format of args: <crawl_id> <time interval between requests in seconds> <# of sites visited> <# of peers>)
thread = threading.Thread(target=start_peer, args=(p,))
thread.start()
thread = threading.Thread(target=start_crawl, args=(crawl_id, 1, 100, 1))
thread.start()

# crawl 2: ...
crawl_id += 1
