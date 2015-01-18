# crawl to gather data about our requests vs peer requests to help with learning algorithm

# usage: (1) python basic_multisurf_peer.py 12345 (if one peer)
#            python basic_multisurf_peer.py 12345 ; python basic_multisurf_peer.py 12346 (if two peers)
#        (2) python collect.py <crawl_id> <time interval between requests in seconds> <# of sites visited> <username>

import sys
import os
import csv
from threading import Thread
from time import sleep
import client
import paramiko

######## Helper functions ########

# get 100 sites from alexa top sites
def get_sites(n):
    alexa_sites = []
    #print "Starting to get sites..."
    with open('top-1m.csv', 'rb') as f:
        reader = csv.reader(f)
        r = list(reader)
        #print "Created reader..."
        for item in r:
            # change to 501 for Alexa 500
            if item[0] == n:
                break
            else:
                #print "Appending www."+item[1]
                alexa_sites.append("www."+item[1])
    return alexa_sites

# visit the <url> <freq> times in <timeout> intervals
def make_req(url, crawl_id, client_id, run, freq, timeout):
    for i in range (0, freq):
        result = client.doCrawl(url, 'localhost', 12345)
        if result == 0:
            pass
            #print "Something is wrong.  Don't include in database"
        elif type(result) == int:
            error = url+" "+str(i)+" "+str(result)
            write_error_results(run, crawl_id, client_id, error)
            #print "Something is wrong.  Don't include in database"
        else:
            request = result[1]
            response_body = result[0]
            write_results_to_file(run, client_id, crawl_id, i, url, request, response_body)
        sleep(float(timeout))

# writes the results of request to local files
# cron job on cs server grabs these and deletes them
def write_results_to_file(run, client_id, crawl_id, visit_id, url, request_hdr, response_body):

    fullpath = '/home/princeton_multisurf/crawl_data/'+run

    # ensure the run directory exists
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)

    #print "Starting to write"
    f1 = open(fullpath+'/'+str(client_id)+'_'+str(crawl_id)+'_'+str(visit_id)+'_request_'+url, 'w+')
    f2 = open(fullpath+'/'+str(client_id)+'_'+str(crawl_id)+'_'+str(visit_id)+'_body_'+url, 'w+')
    encoded_hdr = request_hdr.encode('base64','strict')
    f1.write(encoded_hdr.replace('\n', ''))
    encoded_body = response_body.encode('base64','strict')
    f2.write(encoded_body.replace('\n', ''))
    #stdin, stdout, stderr = client.exec_command(cmd)
    f1.close()
    f2.close()
    print run+": Wrote file for "+str(client_id)+" "+str(crawl_id)+" "+str(visit_id)+" "+url
    
def write_error_results(run, crawl_id, client_id, error):
    #str1 = '\n'.join(str(x) for x in error_list)
    str1 = error

    fullpath = '/home/princeton_multisurf/'+run

    # ensure the run directory exists
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)

    #print "Starting to write"
    f = open(fullpath+'/'+str(client_id)+'_'+str(crawl_id)+'_error_list', 'a+')
    #encoded = str1.encode('base64','strict')
    #f.write(encoded.replace('\n', ''))
    f.write(str1+'\n')
    #stdin, stdout, stderr = client.exec_command(cmd)
    f.close()
    #error_list = [] # reset error list
    print run+": Wrote error file for "+str(client_id)+" "+str(crawl_id)

######## Start script ########

sites = get_sites(sys.argv[3])
#print "Got sites..."

crawl_id = sys.argv[1]
timeout = sys.argv[2]
run_name = sys.argv[4]
client_id = sys.argv[5]
freq = int(sys.argv[6])

# starts a new thread for each site
count = 1
for s in sites:
    #print s
        t = Thread(target=make_req, args=(s, crawl_id, client_id, run_name, 
                                          freq, timeout))
        t.start()
