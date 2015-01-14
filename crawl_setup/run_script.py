# installs python and deploys the crawler scripts on a list of planet lab nodes

import sys
from subprocess import call
import paramiko
from threading import Thread, current_thread

# get the name of the script to run
flag = str(sys.argv[1])
script = str(sys.argv[2])

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
            
# runs the given script on the remote node
def run_script_remote(node):
    print current_thread().name+": Execution of "+script+".sh on node "+node+" started."
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(node, username='princeton_multisurf')
    
    channel = client.invoke_shell()
    channel.send('sudo chmod 744 '+script+'.sh\n')
    out = ''
    while not out.endswith('$ '):
        resp = channel.recv(1024)
        out += resp

    # Reading the output back seems to be the only way to 
    # make sure the update finishes
    channel.send('./'+script+'.sh\n')
    out = ''
    while not out.endswith('$ '):
        resp = channel.recv(1024)
        out += resp

    #add the newline to the node output
    out += '\n'

    # write the update's output to a log file, just for sanity
    f = open(node+'_'+script+'.log', 'wb')
    f.write(out)
    f.close()

    client.close()
    print current_thread().name+": Finished on node "+node+"\nCheck this node's script log file to make sure there were no errors."   
    
# run the given script locally, assumes the script takes the specific node as an arg
def run_script_local(node):
    print current_thread().name+": Update to node "+node+" started."
    call(['./'+script+'.sh', node])
    print current_thread().name+": Finished update of node "+node 

nodes = get_nodes()

for n in nodes:
    if (flag == '-l'):
        t = Thread(target=run_script_local, args=(n,))
        t.start()
    elif (flag == '-r'):
        t = Thread(target=run_script_remote, args=(n,))
        t.start()
    
