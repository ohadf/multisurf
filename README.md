multisurf
=========

Running web data collection:
- Specify each crawl in *run_crawls.py* as follows:
```
    t = Thread(target=remote_crawl, args=(<crawl ID from util.py>, <interval>, <num sites>, n, <num visits>))
    t.start()
```
- Transfer modified *run_crawls.py* to CS server if the script was modified locally
- Run: ```python run_crawls.py <run name>```
