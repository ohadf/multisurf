Here are instructions for collecting web data on a set of PlanetLab nodes, from setting them up with the necessary software to running the data collection on the cycles servers.

#Managing the PlanetLab nodes

The following tasks are all performed on a set of PlanetLab nodes specified
in *nodes.txt*. This list contains the hostnames of all nodes (one per line)
to be included in a given task. To exclude a node from the task add the 
"#" symbol at the beginning of the corresponding line in *nodes.txt*.

##Preparing nodes for the web data collection:
- Run: ```python run_script.py -l deploy_updater```
- Run: ```python run_script.py -r update```
- Check whether Python2.7 is installed
- If not, run: ```python run_script.py -r install_python```

##Deploying the crawler (must do this if the crawler software has been modified):
- Run: ```python run_script.py -l deploy_crawler```

#Collecting data on the Cycles servers

##Setting up the web data collection:
- Specify each crawl in *run_crawls.py* as follows:
```
t = Thread(target=remote_crawl, args=(<crawl ID from util.py>, <interval>, <num sites>, n, <num visits>))
t.start()
```
- Copy the files necessary for the crawls to your home directory on cycles: ```./setup_cycles.sh <username>```

##Running web data collection:
- Install paramiko if you have not already: ```pip install --user paramiko```
- Open a new screen terminal: ```screen```
- Change the Python path to find paramiko: ```export PYTHONPATH=/u/<username>/.local/lib/python3.3/site-packages```
- Run the cron job: ```crontab cron.txt```
- Start the crawl (w/o email notification): ```python run_crawls.py <run name>```
- Start the crawl w/ email notification: ```python run_crawl.py <run name>; mail -s "Multisurf Crawl Done" <username>@cs.princeton.edu < /dev/null```
- After crawl has started, detach the screen window: ```Crtl-A d``` .It is now safe to logout of cycles.
- To check on progress: ssh back into cycles and type ```screen -r```

##Wrapping up the web data collection:
- Remove the cronjob: ```crontab -r```
- Delete the screen terminal: From within the running terminal run ```Ctrl-a k``` or ```Cmd-a k``` on a Mac, and type "yes"
