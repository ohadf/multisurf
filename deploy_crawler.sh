#!/bin/bash
rsync -rz --progress --exclude '*.pyc' --exclude '*~' ./crawls/* princeton_multisurf@planetlab1.csuohio.edu:~/crawls
rsync -rz --progress run_crawl.sh princeton_multisurf@planetlab1.csuohio.edu:~
