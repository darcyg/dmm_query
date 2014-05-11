# Scrapy settings for dmm_query project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'dmm_query'

SPIDER_MODULES = ['dmm_query.spiders']
NEWSPIDER_MODULE = 'dmm_query.spiders'
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ja',
    'Referer': 'http://www.google.com'
}

COOKIES_DEBUG = False

ITEM_PIPELINES = {
  'dmm_query.pipelines.JsonWriterPipeline': 100,
  'dmm_query.pipelines.ContentCreatorPipeline': 200,
  'dmm_query.pipelines.FinalizerPipeline': 1000
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'dmm_query (+http://www.yourdomain.com)'
