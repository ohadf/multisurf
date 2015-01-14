#!/bin/bash
rsync -rz --progress update.sh princeton_multisurf@$1:~
rsync -rz --progress install_python.sh princeton_multisurf@$1:~
