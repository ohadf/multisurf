# only deploys the crawler scripts to a list of planet lab nodes

import sys
from subprocess import call
import paramiko
from threading import Thread, current_thread

# get list of nodes
def get_nodes():
    nodes = []
    #print "Starting to get sites..."
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

#rsyncs the crawl files on the given node
def update(node):
    print current_thread().name+": Update to node "+node+" started."
    call(['./deploy_crawler.sh', node])
    print current_thread().name+": Finished update of node "+node

nodes = get_nodes()

for n in nodes:
    t = Thread(target=update, args=(n,))
    t.start()
