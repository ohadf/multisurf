# script to do a number of crawls using collect.py

# usage: python master_crawl.py <username> <client_id>

import os
import threading
from time import mktime
import sys
import getpass
import datetime

def start_crawl(a,b,c,d,e,f,g):
    os.system("python collect.py "+str(a)+" "+str(b)+" "+str(c)+" "+str(d)+" "+str(e)+" "+str(f)+" "+str(g))

# gets the current time in milliseconds since epoch
# this timestamp is included in every file
def get_current_time_millis():
    now = datetime.datetime.utcnow()
    millis = long(mktime(now.timetuple())*1000 + (now.microsecond/1000))
    return millis

crawl_id = 1
client_id = sys.argv[2]

user = sys.argv[1]
pwd = getpass.getpass()

timestamp = get_current_time_millis()

# crawl 1: 1 second time interval, 300 sites
thread = threading.Thread(target=start_crawl, args=(crawl_id, 1, 300, user, pwd, client_id, timestamp))
thread.start()

# crawl 2: 60 seconds between requests, 300 sites (format of args: <crawl_id> <time interval between requests in seconds> <# of sites visited> <# of peers>)
crawl_id += 1
thread = threading.Thread(target=start_crawl, args=(crawl_id, 60, 300, user, pwd, client_id, timestamp))
thread.start()

# crawl 3: 300 seconds between requests, 300 sites (format of args: <crawl_id> <time interval between requests in seconds> <# of sites visited> <# of peers>)
crawl_id += 1
thread = threading.Thread(target=start_crawl, args=(crawl_id, 300, 300, user, pwd, client_id, timestamp))
thread.start()

# crawl 4: two peers on local machine, 600 seconds between requests, 300 sites (format of args: <crawl_id> <time interval between requests in seconds> <# of sites visited> <# of peers>)
crawl_id += 1
thread = threading.Thread(target=start_crawl, args=(crawl_id, 600, 300, user, pwd, client_id, timestamp))
thread.start()
