from sample.spiders import CommonSampleSpider
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log

class FlickrSpider(CommonSampleSpider):
    def __init__(self):
        self.start_urls = ['http://www.flickr.com/photos/tags/']
        super(FlickrSpider,self).__init__()

    domain_name = 'flickr.com'

    rules = (
            Rule(SgmlLinkExtractor(allow=(r'photos/.+/[0-9]+/',)), callback='parse_item'),
            Rule(SgmlLinkExtractor(allow=('photos/tags',)))
    )

    def parse_item(self,response):
        log.msg('parse_item called for url : %s' % response.url)

SPIDER = FlickrSpider()
