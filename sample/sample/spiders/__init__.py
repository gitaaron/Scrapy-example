# This package will contain the spiders of your Scrapy project
#
# To create the first spider for your project use this command:
#
#   scrapy-ctl.py genspider myspider myspider-domain.com
#
# For more info see:
# http://doc.scrapy.org/topics/spiders.html

import os,pickle
from scrapy.contrib.spiders import CrawlSpider
from scrapy.conf import settings
from scrapy.xlib.pydispatch import dispatcher
from scrapy.core import signals
from scrapy import log
from scrapy.http import TextResponse


class CommonSampleSpider(CrawlSpider):
    """
    A base spider for storing a running list of most recent pending requests and reading/writing them from disk.
    """
    def __init__(self): 
        self.recent_requests = [] # updated by requestsaver scheduler middleware for restarting approximately where we left off
        dir_path = settings.get('PATH_TO_REQUEST_LOG')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        self.request_log_path = os.path.join(dir_path,self.__class__.__name__.lower() + '.log')
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

        super(CommonSampleSpider, self).__init__()

    def __unicode__(self):
        return u'%s' % self.__class__()

    def _get_start_urls(self):
        """ 
        If most recent requests were found, use those otherwise start from the beginning.
        """ 
        try:
            log.msg('trying : %s' % self.request_log_path)
            f = open(self.request_log_path,'r')
            pickled_data = f.read()
            f.close()
            data = pickle.loads(pickled_data)
            return data
        except (IOError,EOFError):
            return None


    def start_requests(self):
        '''
        If there are no recent_urls to be read from the previous crawl, then return the spider's start_urls.
        Otherwise create a dummy response full of urls to be parsed by the link extractor for generating the 
        appriopriate requests with their callbacks.
        '''
        recent_urls = self._get_start_urls()
        if recent_urls:
            reqs = []
            # ensure that spider is open
            # otherwise if I pass requests with callbacks at this point,
            # a keyerror is thrown in enqueue_scrape
            from scrapy.core.engine import scrapyengine
            scrapyengine.open_spider(self)


            while len(recent_urls) > settings.get('RECENT_URLS_SIZE',300):
                recent_urls.pop(0)


            first_url = recent_urls[0]

            log.msg('first_url : %s' % first_url, level=log.ERROR)

            body = ''
            for url in recent_urls:
                body+= '<a href="' + url + '"></a>'
            dummy_response = TextResponse(first_url,body=body)
            reqs.extend(self._requests_to_follow(dummy_response))
            return reqs
        else:
            return super(CommonSampleSpider, self).start_requests()



    def spider_closed(self):
        """
        Write the recent request list to the log path.
        """
        if self.request_log_path:
            f = open(self.request_log_path,'w')
            f.write(pickle.dumps(self.recent_requests))
            f.close()
        else:
            log.msg('%s not found when trying to close spider'%request_log_path,level=log.ERROR)


