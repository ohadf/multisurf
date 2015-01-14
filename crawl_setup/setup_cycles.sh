#!/bin/bash
rsync -rz --progress cron.txt nodes.txt retrieve_files.py run_crawls.py $1@tux.cs.princeton.edu:~
