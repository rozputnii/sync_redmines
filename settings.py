"""Settings file for project"""

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

try:
    module = __import__('settings_local', globals(), locals(), ['*'])
    for k in dir(module):
        locals()[k] = getattr(module, k)
except ImportError:
    pass
