# runs the multisurf crawls on all planet lab nodes

import sys
import paramiko
import select
from threading import Thread, current_thread

# get list of nodes
def get_nodes():
    nodes = []
    f = open('nodes.txt', 'r')
    count = 0
    for node in f:
        if node.startswith('#'):
            print(node.strip())
        else:
            count += 1
            nodes.append(node.strip())
    print("Collecting site data from "+str(count)+" nodes")
    return nodes
            
#usage: python run_crawls.py <username> <run_name>

# runs the crawl on the given node
def remote_crawl(crawl_id, timeout, num_sites, node, freq):
    try: 
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        client.connect(node, username='princeton_multisurf')
    except:
        print("Could not connect to node "+node)
        sys.exit(1)

    #Send the command
    stdin, stdout, stderr = client.exec_command('cd ./crawls; python collect.py '+str(crawl_id)+' '+str(timeout)+' '+str(num_sites)+' '+run_name+' '+node+' '+str(freq))

    print ("Starting crawl type "+str(crawl_id)+" on node "+node)

    f = open(node+'_crawl.log', 'ab+')

    # wait for the command to terminate
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            r1, w1, x1 = select.select([stdout.channel], [], [], 0.0)
            if len(r1) > 0:
                f.write(stdout.channel.recv(1024))

    '''
    channel = client.invoke_shell()
    channel.send('cd ./crawls\n')
    out = ''
    while not out.endswith('$ '):
        resp = channel.recv(1024)
        out += str(resp)
    
    print ("Starting crawl type "+str(crawl_id)+" on node "+node)

    # Reading the output back seems to be the only way to 
    # make sure the update finishes
    channel.send('python collect.py '+str(crawl_id)+' '+str(timeout)+' '+str(num_sites)+' '+run_name+' '+node+' '+str(freq)+'\n')
    out = ''

    while not out.endswith('$ '): 
        resp = channel.recv(1024)
        out += str(resp)

    # write the crawler's output to a log file, just for sanity
    f = open(node+'_crawl.log', 'w+')
    f.write(out)
    f.close()
    '''

    client.close()
    f.close()
    print ("Finished crawl type "+str(crawl_id)+" on node "+node)

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
    
