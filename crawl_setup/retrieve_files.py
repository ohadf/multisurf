# scps all files from planetlab nodes to cycles servers and deletes the files on planetlab nodes

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
            print (node.strip())
        else:
            count += 1
            nodes.append(node.strip())
    print ("Updating "+str(count)+" nodes")
    return nodes

#scps the crawl files to cycles
def scp(node):
    print (current_thread().name+": scp-ing file from node "+node+"...")
    call(["scp -r", "princeton_multisurf@"+node+":~/crawl_data/", "/n/fs/multisurf/"])
    print (current_thread().name+": Done scp-ing from node "+node)
    print (current_thread().name+": deleting files from node "+node)
    delete_files(node)
    print (current_thread().name+": Done deleting files from node "+node)

# deletes all files in the crawls folder on a planetlab node
def delete_files(node):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(node, username='princeton_multisurf')
    
    channel = client.invoke_shell()
    channel.send('rm -rf ~/crawl_data/\n')
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


nodes = get_nodes()

for n in nodes:
    t = Thread(target=scp, args=(n,))
    t.start()
    
