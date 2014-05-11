#!/usr/bin/env python
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log
from dmm_query.spiders.dmm_query_spider import DmmQuerySpider
from dmm_query.spiders.dmm_direct_spider import DmmDirectSpider
from dmm_query.spiders.dmm_batch_query_spider import DmmBatchQuerySpider 
from scrapy.utils.project import get_project_settings
import sys

def setup_crawler():
    spider = DmmDirectSpider(url=sys.argv[1])
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

setup_crawler()
log.start()
reactor.run()

