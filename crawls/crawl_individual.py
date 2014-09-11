# usage: python crawl_individual.py <crawl_id>

import requests
import sys
import time
import httplib
from threading import Thread
import csv

# get 100 sites from alexa top sites
def get_sites():
    alexa_sites = []
    with open('top-1m.csv', 'rb') as f:
        reader = csv.reader(f)
        r = list(reader)
        for item in r:
            # change to 501 for Alexa 500
            if item[0] == '101':
                break
            else:
                alexa_sites.append("www."+item[1])
    return alexa_sites

def make_req(u, n):
    # info for us
    response = requests.get('http://'+u)
    crawl_id = sys.argv[1]
    t = time.time()
    thread_id = n
    url = response.url
    req_headers = response.request.headers.items()
    stat_code = response.status_code
    headers = response.headers
    history = response.history
    body = response.text
    print url, thread_id

    # TODO: info for peer
        # 1. send request to peer
        # 2. wait for response
        # 3. get all info from response



######## Start script ########

sites = get_sites()

# starts a new thread for each site
count = 1
for s in sites:
    t = Thread(target=make_req, args=(s,count,))
    t.start()
    count += 1


