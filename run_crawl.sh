#!/bin/bash

if [ "$#"-ne 3 ]; then
	echo "usage: ./run_crawl.sh <cs username> <client id>"
fi

cd ./crawls
python master_crawl.py $1 $2