#!/bin/bash
rsync -rz --progress --exclude '*.pyc' --exclude '*~' ./crawls/* princeton_multisurf@planetlab1.csuohio.edu:~
