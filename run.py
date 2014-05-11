#!/usr/bin/env python
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log
from dmm_query.spiders.dmm_query_spider import DmmQuerySpider
from dmm_query.spiders.dmm_batch_query_spider import DmmBatchQuerySpider 
from scrapy.utils.project import get_project_settings

def setup_crawler():
    spider = DmmQuerySpider(id="550", publisher="rbd")
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

setup_crawler()
log.start()
reactor.run()

