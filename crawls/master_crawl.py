# script to do a number of crawls using collect.py

# usage: python master_crawl.py <username> <client_id>

import os
import threading
from time import mktime
import sys
import getpass
import datetime
import util

def start_crawl(a,b,c,d,e,f,g):
    os.system("python collect.py "+str(a)+" "+str(b)+" "+str(c)+" "+str(d)+" "+str(e)+" "+str(f)+" "+str(g))

# gets the current time in milliseconds since epoch
# this timestamp is included in every file
def get_current_time_millis():
    now = datetime.datetime.utcnow()
    millis = long(mktime(now.timetuple())*1000 + (now.microsecond/1000))
    return millis

client_id = sys.argv[3]

user = sys.argv[1]
run_name = sys.argv[2]

# crawl 1: 300 seconds between requests, 300 sites (format of args: <crawl_id> <time interval between requests in seconds> <# of sites visited> <# of peers>)
freq = 15
thread = threading.Thread(target=start_crawl, args=(ONCE_PER_5MIN, 300, 300, user, run_name, client_id, freq))
thread.start()

# crawl 2: two peers on local machine, 600 seconds between requests, 300 sites (format of args: <crawl_id> <time interval between requests in seconds> <# of sites visited> <# of peers>)
freq = 5
thread = threading.Thread(target=start_crawl, args=(ONCE_PER_10MIN, 600, 300, user, run_name, client_id, freq))
thread.start()
