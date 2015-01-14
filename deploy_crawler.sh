#!/bin/bash
rsync -rz --progress --exclude '*.pyc' --exclude '*~' ./crawls/* princeton_multisurf@$1:~/crawls
