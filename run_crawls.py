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
    stdin, stdout, stderr = client.exec_command('cd ./crawls')
    stdin, stdout, stderr = client.exec_command('python master_crawl.py melara '+node)
    stdin.write('password\n')
    stdin.flush()
    print stdout.read()
    print stderr.read()
    client.close()

nodes = get_nodes()

for n in nodes:
    t = Thread(target=crawl, args=(n,))
    t.start()
    
