# runs the multisurf crawls on all planet lab nodes

import sys
import paramiko
from threading import Thread, current_thread

# get list of nodes
def get_nodes():
    nodes = []
    f = open('nodes.txt', 'rb')
    count = 0
    for node in f:
        if node.startswith('#'):
            print node.strip()
        else:
            count += 1
            nodes.append(node.strip())
    print "Collecting site data from "+str(count)+" nodes"
    return nodes
            
#usage: python run_crawls.py <username> <run_name>

# runs the crawl on the given node
def remote_crawl(crawl_id, timeout, num_sites, node, freq):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    print "Starting crawl type "+str(crawl_id)+" on node "+node
    client.connect(node, username='princeton_multisurf')

    channel = client.invoke_shell()
    channel.send('cd ./crawls\n')
    out = ''
    while not out.endswith('$ '):
        resp = channel.recv(1024)
        out += resp

    # Reading the output back seems to be the only way to 
    # make sure the update finishes
    channel.send('python collect.py '+str(crawl_id)+' '+str(timeout)+' '+str(num_sites)+' '+run_name+' '+node+' '+str(freq)+'\n')
    out = ''

    while not out.endswith('$ '): 
        resp = channel.recv(1024)
        out += resp

    # write the crawler's output to a log file, just for sanity
    f = open(node+'_crawl.log', 'wb')
    f.write(out)
    f.close()

    client.close()
    print "Finished crawl type "+str(crawl_id)+" on node "+node

nodes = get_nodes()
run_name = sys.argv[1]

# this code replaces master_crawl.py on the remote host
# call remote_crawl with appropriate params, look at util.py in crawls dir for crawl id
for n in nodes:
    # crawl 1: 300 seconds between requests, 300 sites
    t1 = Thread(target=remote_crawl, args=(5, 300, 300, n, 15))
    t1.start()

    # crawl 2: 600 seconds between requests, 300 sites
    t2 = Thread(target=remote_crawl, args=(6, 600, 300, n, 5))
    t2.start()
    
