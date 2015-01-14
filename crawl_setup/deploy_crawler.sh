#!/bin/bash
rsync -rz --progress --exclude '*.pyc' --exclude '*~' ../crawler/* princeton_multisurf@$1:~/crawls
