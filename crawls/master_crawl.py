# script to do a number of crawls using collect.py

# usage: python master_crawl.py <username> <client_id>

import os
import threading
import time
import sys
import getpass

def start_crawl(a,b,c,d,e,f):
    os.system("python collect.py "+str(a)+" "+str(b)+" "+str(c)+" "+str(d)+" "+str(e)+" "+str(f))

crawl_id = 1
client_id = sys.argv[2]

user = sys.argv[1]
pwd = getpass.getpass()

# crawl 1: 1 second time interval, 300 sites
thread = threading.Thread(target=start_crawl, args=(crawl_id, 1, 20, user, pwd, client_id))
thread.start()

# crawl 2: 60 seconds between requests, 300 sites (format of args: <crawl_id> <time interval between requests in seconds> <# of sites visited> <# of peers>)
'''crawl_id += 1
thread = threading.Thread(target=start_crawl, args=(crawl_id, 60, 300, user, pwd, client_id))
thread.start()

# crawl 3: 300 seconds between requests, 300 sites (format of args: <crawl_id> <time interval between requests in seconds> <# of sites visited> <# of peers>)
crawl_id += 1
thread = threading.Thread(target=start_crawl, args=(crawl_id, 300, 300, user, pwd, client_id))
thread.start()

# crawl 4: two peers on local machine, 600 seconds between requests, 300 sites (format of args: <crawl_id> <time interval between requests in seconds> <# of sites visited> <# of peers>)
crawl_id += 1
thread = threading.Thread(target=start_crawl, args=(crawl_id, 600, 300, user, pwd, client_id))
thread.start()
'''
