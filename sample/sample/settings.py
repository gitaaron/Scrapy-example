# Scrapy settings for sample project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
# Or you can copy and paste them from where they're defined in Scrapy:
# 
#     scrapy/conf/default_settings.py
#

BOT_NAME = 'sample'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['sample.spiders']
NEWSPIDER_MODULE = 'sample.spiders'
DEFAULT_ITEM_CLASS = 'sample.items.SampleItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

# settings I have added in for debugging purposes
DOWNLOAD_DELAY = 10.0 # for making the log readable
REQUESTS_QUEUE_SIZE = 3000
SCHEDULER_ORDER = 'DFO'


# settings required for persisting pending urls
SCHEDULER_MIDDLEWARES = {'sample.middlewares.RequestSaverSchedulerMiddleware':501}
PATH_TO_REQUEST_LOG = '/path/to/project/logs/'
