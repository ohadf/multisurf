# runs the multisurf crawls on all planet lab nodes

import sys
import paramiko
from threading import Thread

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
    print "Updating "+str(count)+" nodes"
    return nodes
            
# runs the crawl on the given node
def crawl(node):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    #print "Trying to connect..."
    client.connect(node, username='princeton_multisurf')

    channel = client.invoke_shell()
    channel.send('cd ./crawls\n')
    out = ''
    while not out.endswith('$ '):
        resp = channel.recv(1024)
        out += resp

    # Reading the output back seems to be the only way to 
    # make sure the update finishes
    channel.send('python master_crawl.py melara '+node+'\n')
    out = ''
    # looks silly, but we can't assume upper- or lower-case P
    while not out.endswith('assword: '): 
        resp = channel.recv(1024)
        out += resp

    # replace with your password here.
    # DON'T FORGET TO REMOVE YOUR PASSWORD WHEN YOU'RE DONE
    channel.send('password\n')

    # looks silly, but we can't assume upper- or lower-case P
    while not out.endswith('$: '): 
        resp = channel.recv(1024)
        out += resp

    # write the crawler's output to a log file, just for sanity
    f = open(node+'_crawl.log', 'wb')
    f.write(out)
    f.close()

    client.close()

nodes = get_nodes()

for n in nodes:
    t = Thread(target=crawl, args=(n,))
    t.start()
    
