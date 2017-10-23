# sync_redmines
Script for synchronize redmine issues and logtimes to another redmine.

* Create file settings_local.py
* Add next settings (use api KEY or USERNAME/PASSWORD):
```python
SRC_URL = ''
SRC_KEY = ''
SRC_PROJECT = ''
SRC_USERNAME = ''
SRC_PASSWORD = ''

DST_URL = ''
DST_KEY = ''
DST_PROJECT = ''
DST_USERNAME = ''
DST_PASSWORD = ''
```
* Call `python sync.py 2017-10-10 2017-10-20` for example
