# crawl to gather data about our requests vs peer requests to help with learning algorithm

# usage: (1) python basic_multisurf_peer.py 12345 (if one peer)
#            python basic_multisurf_peer.py 12345 ; python basic_multisurf_peer.py 12346 (if two peers)
#        (2) python collect.py <crawl_id> <time interval between requests in seconds> <# of sites visited> <username>

import sys
import csv
from threading import Thread
import datetime
import MySQLdb
from time import sleep
import client
import subprocess
import paramiko
import getpass

######## Helper functions ########

# get 100 sites from alexa top sites
def get_sites(n):
    alexa_sites = []
    print "Starting to get sites..."
    with open('top-1m.csv', 'rb') as f:
        reader = csv.reader(f)
        r = list(reader)
        print "Created reader..."
        for item in r:
            # change to 501 for Alexa 500
            if item[0] == n:
                break
            else:
                print "Appending www."+item[1]
                alexa_sites.append("www."+item[1])
    return alexa_sites

# x: url, c_id: crawl_id, th_id: thread_id
def make_req(x, c_id, th_id):
    crawl_id = c_id
    timestamp = datetime.datetime.utcnow()
    thread_id = th_id
    url = x
    result = client.doCrawl(x, 'localhost', 12345)
    if result == 0:
        print "Something is wrong.  Don't include in database"
    elif type(result) == int:
        print "Something is wrong.  Don't include in database"
    else:
        request = result[1]
        response_body = result[0]
        write_results_to_file(crawl_id, thread_id, url, request, response_body)

def ssh_helper(cmd):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    print "Trying to connect..."
    client.connect("tux.cs.princeton.edu", username=username, password=password)
    stdin, stdout, stderr = client.exec_command(cmd)
    print "Finished command"
    client.close()

# writes the results of request to files
def write_results_to_file(crawl_id, thread_id, url, request_hdr, response_body):
    print "Starting to write"
    #print '/n/fs/multisurf/body_'+url
    ssh_helper('echo "'+response_body.encode('base64','strict')+'" > /n/fs/multisurf/'+str(crawl_id)+'_'+str(thread_id)+'_body_'+url)
    ssh_helper('echo "'+request_hdr.encode('base64','strict')+'" > /n/fs/multisurf/'+str(crawl_id)+'_'+str(thread_id)+'_request_'+url)

######## Start script ########

password = getpass.getpass()

sites = get_sites(sys.argv[3])
print "Got sites..."

username = sys.argv[4]

# starts a new thread for each site
count = 1
for s in sites:
    print s
    t = Thread(target=make_req, args=(s, sys.argv[1], count))
    t.start()
    count += 1
    sleep(float(sys.argv[2]))
