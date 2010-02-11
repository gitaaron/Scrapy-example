#import sys,traceback,datetime

from scrapy.conf import settings


class RequestSaverSchedulerMiddleware(object):

    def enqueue_request(self,spider,request):
        spider.recent_requests.append(request.url)
        while len(spider.recent_requests) > settings.get('RECENT_URLS_SIZE',300):
            spider.recent_requests.pop(0)
        return None
