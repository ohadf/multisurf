# installs python and deploys the crawler scripts on a list of planet lab nodes

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

def install(node):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(node, username='princeton_multisurf')
    
    channel = client.invoke_shell()
    channel.send('sudo chmod 744 update.sh\n')
    out = ''
    while not out.endswith('$ '):
        resp = channel.recv(1024)
        out += resp

    # Reading the output back seems to be the only way to 
    # make sure the update finishes
    channel.send('./update.sh\n')
    out = ''
    while not out.endswith('$ '):
        resp = channel.recv(1024)
        out += resp

    #add the newline to the node output
    out += '\n'

    # write the update's output to a log file, just for sanity
    f = open(node+'_update.log', 'wb')
    f.write(out)
    f.close()

    client.close()

#rsyncs the crawl files and installs python on the given node
def update(node):
    print current_thread().name+": Update to node "+node+" started."
    call(['./deploy_crawler.sh', node])
    install(node)
    print current_thread().name+": Finished update of node "+node+"\nCheck this node's update.log file to make sure there were no errors."

nodes = get_nodes()

for n in nodes:
    t = Thread(target=update, args=(n,))
    t.start()
    
