# scrape all the scripts and compare

import sys
import os.path
import csv
import json
from bs4 import BeautifulSoup

# spatial comparison:
# want to scrape the scripts from each response body
# for each website, for each crawl_ID and run_ID

# get n sites from alexa top sites
def get_sites(n="301"):
    alexa_sites = []
    #print "Starting to get sites..."
    with open('top-1m.csv', 'rb') as f:
        reader = csv.reader(f)
        r = list(reader)
        #print "Created reader..."
        for item in r:
            # change to 501 for Alexa 500
            if item[0] == n:
                break
            else:
                #print "Appending www."+item[1]
                alexa_sites.append("www."+item[1])
    return alexa_sites

# get list of nodes
def get_nodes():
    nodes = []
    f = open('nodes.txt', 'r')
    count = 0
    for node in f:
        if not node.startswith('#'):
            count += 1
            nodes.append(node.strip())
    print("Getting script data from "+str(count)+" nodes")
    return nodes

# read in all of the bodies for a given crawl and trial ID
# and scrape all of the scripts
def read_bodies_for_crawl (sites, nodes, run, crawl_id, trial_id):
    scripts = dict()
    # for each site
    for site in sites:
        site_scripts = dict()
        
        # for each node
        for node in nodes:
            #print("Reading body for site "+site+" for node "+node)

            # if we have a file for the given node, crawl_id and trial_id
            fname = node+"_"+str(crawl_id)+"_"+str(trial_id)+"_"+"body_"+site

            if os.path.isfile("/n/fs/multisurf/"+run+"/"+fname):
                print("scraping")
                # get the entire response body
                f = open("/n/fs/multisurf/"+run+"/"+fname)
                body = f.read().decode('base64','strict')
                f.close()
                # and scrape all of the scripts
                soup = BeautifulSoup(body)
                site_scripts[node] = soup.find_all('script')

        scripts[site] = site_scripts
    return scripts

# now we compare each script for each site for each node
def compare_scripts (scripts):
    scripts_diff = dict()
    # loop over all keys (i.e. sites) in the scripts dict
    for site in scripts:
        site_scripts = scripts[site]
        site_scripts_diff = dict()
        
        if len(site_scripts) == 0:
            scripts_diff[site] = "No scripts found"
        else:
            # now we compare each node with each other
            for node1 in site_scripts:
                scripts_list1 = set(site_scripts[node1])
                node1_diff = site_scripts_diff[node1] = dict()
                
                for node2 in site_scripts :
                    # we don't want to compare ourselves with ourselves
                    if node1 != node2:
                        print("Comparing "+node1+" and "+node2+" for site "+site)
                        scripts_list2 = set(site_scripts[node2])
                        
                        # this records all scripts that are in node2's view not in node1's list
                        diff = list(scripts_list2.difference(scripts_list1))
                        
                        node1_diff[node2] = diff
            scripts_diff[site] = site_scripts_diff
    return scripts_diff

''' Here's where the main script starts '''

if len(sys.argv) < 6 :
    print "Usage: python script_diffs <run_name> <crawl_id> <trial_id> <output filename> [num_sites]"
    exit()

run_name = sys.argv[1]
crawl_id = sys.argv[2]
trial_id = sys.argv[3]
outfile = sys.argv[4]
sites = get_sites(sys.argv[5])
nodes = get_nodes()
scripts = read_bodies_for_crawl(sites, nodes, run_name, crawl_id, trial_id)
script_diffs = compare_scripts(scripts)

out = open("/n/fs/multisurf/"+outfile, 'w+')
# print pretty JSON
out.write(json.dumps(script_diffs, sort_keys=True, indent=4, separators=(",", ": ")))
out.close()

                    
                                
                            
                        
                            
                            
                                
                                
                                
                            
