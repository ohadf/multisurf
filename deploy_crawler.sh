#!/bin/bash
rsync -rz --progress --exclude '*.pyc' --exclude '*~' ./crawls/* princeton_multisurf@$1:~/crawls
rsync -rz --progress update.sh princeton_multisurf@$1:~
