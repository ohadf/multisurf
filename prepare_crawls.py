# installs python on a list of planet lab nodes

import sys
from subprocess import call
import paramiko
from threading import Thread

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
            
# installs python and paramiko on the given node
def install(node):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    #print "Trying to connect..."
    client.connect(node, username='princeton_multisurf')
    stdin, stdout, stderr = client.exec_command('chmod 744 update.sh')
    stdin, stdout, stderr = client.exec_command('./update.sh')
    print stdout.read()
    print stderr.read()
    client.close()

#rsyncs the crawl files and installs python on the given node
def update(node):
    print "Update to node "+node+" started."
    call(['./deploy_crawler.sh', node])
    install(node)
    print "Successfully updated "+node

nodes = get_nodes()

for n in nodes:
    t = Thread(target=update, args=(n,))
    t.start()
    
