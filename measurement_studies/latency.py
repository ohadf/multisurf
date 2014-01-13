import sys
import basic_multisurf_client
import csv
import os
import util
import comparisons
from random import randrange
import time

def get_baseline_latency():
    start = time.time()
    basic_multisurf_client.measure_baseline_latency(sys.argv[1],'localhost', 12345)
    end = time.time()
    elapsed = end - start
    print elapsed

def get_num_scripts_latency():
    start = time.time()
    basic_multisurf_client.measure_multisurf_latency(sys.argv[1],'localhost', 12345, 0)
    end = time.time()
    elapsed = end - start
    print elapsed

def get_line_by_line_latency():
    start = time.time()
    basic_multisurf_client.measure_multisurf_latency(sys.argv[1],'localhost', 12345, 1)
    end = time.time()
    elapsed = end - start
    print elapsed

def get_links_latency():
    start = time.time()
    basic_multisurf_client.measure_multisurf_latency(sys.argv[1],'localhost', 12345, 2)
    end = time.time()
    elapsed = end - start
    print elapsed

def get_two_peers_latency():
    start = time.time()
    basic_multisurf_client.measure_multisurf_latency(sys.argv[1],'localhost', 12345, 3)
    end = time.time()
    elapsed = end - start
    print elapsed

def get_all_comparisons_latency():
    start = time.time()
    basic_multisurf_client.measure_multisurf_latency(sys.argv[1],'localhost', 12345, 4)
    end = time.time()
    elapsed = end - start
    print elapsed

get_baseline_latency()

print "***********************"

get_line_by_line_latency()

print "***********************"

get_links_latency()

print "***********************"

get_num_scripts_latency()

print "***********************"
