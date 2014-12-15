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

def mkdir_ssh(node):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(node, username='princeton_multisurf')
    
    channel = client.invoke_shell()
    channel.send('mkdir .ssh\n')
    out = ''
    while not out.endswith('$ '):
        resp = channel.recv(1024)
        out += resp

    #add the newline to the node output
    out += '\n'

    # write the deployment's output to a log file, just for sanity
    f = open('ssh_deploy.log', 'ab')
    f.write(out)
    f.close()

    client.close()

#rsyncs the crawl files and installs python on the given node
def deploy(node):
    print current_thread().name+": Deploying SSH key to node "+node+"..."
    mkdir_ssh(node)
    call(["scp", "./ssh/id_rsa", "princeton_multisurf@"+node+":~/.ssh"])
    call(["scp", "./ssh/id_rsa.pub", "princeton_multisurf@"+node+":~/.ssh"])
    call(["scp", "./ssh/known_hosts", "princeton_multisurf@"+node+":~/.ssh"])
    print current_thread().name+": Done deploying to "+node

nodes = get_nodes()

for n in nodes:
    t = Thread(target=deploy, args=(n,))
    t.start()
    
