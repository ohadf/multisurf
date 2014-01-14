import sys
import basic_multisurf_client
import csv
import os
import util
import comparisons
from random import randrange
import time

def get_baseline_latency(url):
    start = time.time()
    basic_multisurf_client.measure_baseline_latency(url,'localhost', 12345)
    end = time.time()
    elapsed = end - start
    return elapsed

def get_num_scripts_latency(url):
    start = time.time()
    basic_multisurf_client.measure_multisurf_latency(url,'localhost', 12345, 0)
    end = time.time()
    elapsed = end - start
    return elapsed

def get_line_by_line_latency(url):
    start = time.time()
    basic_multisurf_client.measure_multisurf_latency(url,'localhost', 12345, 1)
    end = time.time()
    elapsed = end - start
    return elapsed

def get_links_latency(url):
    start = time.time()
    basic_multisurf_client.measure_multisurf_latency(url,'localhost', 12345, 2)
    end = time.time()
    elapsed = end - start
    return elapsed

def get_two_peers_latency(url):
    start = time.time()
    basic_multisurf_client.measure_multisurf_latency(url,'localhost', 12345, 3)
    end = time.time()
    elapsed = end - start
    return elapsed

def get_all_comparisons_latency(url):
    start = time.time()
    basic_multisurf_client.measure_multisurf_latency(url,'localhost', 12345, 4)
    end = time.time()
    elapsed = end - start
    return elapsed





alexa_sites = []
with open('top-1m.csv', 'rb') as f:
    reader = csv.reader(f)
    r = list(reader)
    for item in r:
        # change to 501 for Alexa 500
        if item[0] == '51':
            break
        else:
            alexa_sites.append("www."+item[1])

avg_elapsed_time = 0.000000
for s in alexa_sites:
    #print "starting client for: "+s
    # 0 - number of scripts; 1 - line by line; 2 - links; 3 - two peers; 4 - combination of comparisons;
    avg_elapsed_time += get_two_peers_latency(s)
    #print "finishing client for: "+s

print avg_elapsed_time/50.000000
#get_baseline_latency()

#print "***********************"

#get_line_by_line_latency()

#print "***********************"

#get_links_latency()

#print "***********************"

#get_num_scripts_latency()

#print "***********************"
