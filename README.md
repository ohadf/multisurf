multisurf
=========

The following tasks are all performed on a set of PlanetLab nodes specified
in *nodes.txt*. This list contains the hostnames of all nodes (one per line)
to be included in a given task. To exclude a node from the task add the 
"#" symbol at the beginning of the corresponding line in *nodes.txt*.

Preparing the PlanetLab nodes for the web data collection:
- Run: ```python run_script.py -r update```
- Check whether Python2.7 is installed
- If not, run: ```python run_script.py -r install_python```

Deploying the crawler (must do this if the crawler software has been modified):
- Run: ```python run_script.py -l deploy_crawler```

Running the cron job:
- Ensure *retrieve_files.py* and *cron.txt* are in your home directory on cycles.
- Run: ```crontab cron.txt```

Running web data collection:
- Specify each crawl in *run_crawls.py* as follows:
```t = Thread(target=remote_crawl, args=(<crawl ID from util.py>, <interval>, <num sites>, n, <num visits>))
t.start()
```
- Transfer modified *run_crawls.py* to CS server if the script was modified locally
- Run: ```python run_crawls.py <run name>```
