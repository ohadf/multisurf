# installs python on a list of planet lab nodes

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
            
# installs python and paramiko on the given node
# using paramiko transport to read the command outputs on the 
# remote machine in real-time
def install(node):
    trans = paramiko.Transport((node, 22))
    trans.connect(username='princeton_multisurf')
    session = trans.open_channel('update session')
    session.exec_command('sudo chmod 744 update.sh')
    session.exec_command('./update.sh')
    while session.recv_ready():
        temp = session.recv(1024)
        print temp
    trans.close()

#rsyncs the crawl files and installs python on the given node
def update(node):
    print current_thread()+": Update to node "+node+" started."
    call(['./deploy_crawler.sh', node])
    install(node)
    print current_thread()": Successfully updated "+node

nodes = get_nodes()

for n in nodes:
    t = Thread(target=update, args=(n,))
    t.start()
    
