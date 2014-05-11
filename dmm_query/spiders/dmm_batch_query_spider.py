# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.selector import Selector
from dmm_query.items import DmmQueryItem
from scrapy.http import Request
from os import listdir
from os.path import isfile, join
import re

class DmmBatchQuerySpider(Spider):
  name = "DmmBatchQuery"
  allowed_domains = ["dmm.co.jp"]
  start_url_template = "http://www.dmm.co.jp/search/=/searchstr=%s%%20%s/n1=FgRCTw9VBA4GAVhfWkIHWw__/n2=Aw1fVhQKX1ZRAlhMUlo5QQgBU1lR/"
  start_urls = ["http://www.dmm.co.jp/top/"]
  start_urls = [
    "http://www.dmm.co.jp/search/=/searchstr=rbd%20550/n1=FgRCTw9VBA4GAVhfWkIHWw__/n2=Aw1fVhQKX1ZRAlhMUlo5QQgBU1lR/"
  ]
  brief_ids = ["rbd550"]
  directory = "/home/pi/dmm_query/dest"

  def __init__(self, directory=None, *args, **kwargs):
    super(DmmBatchQuerySpider, self).__init__(*args, **kwargs)
    self.directory = directory

  def parse(self, response):
    self.start_urls = []
    self.brief_ids = []
    for f in listdir(self.directory):
        if isfile(join(self.directory,f)):
          print f
          m = re.search(r"((.*)-)?(([A-Za-z]+)(-)?([0-9]+)([A-Za-z])?)(.*)\.[A-Za-z0-9]*", f)
          if m:
            print m.groups()[3]
            print m.groups()[5]
            publisherId = m.groups()[3].lower()
            productId = m.groups()[5]
            url = self.start_url_template % (publisherId, productId)
            id = publisherId + productId
            yield Request(url, callback=lambda r, id=id,f=f:self.parseSearch(r,id,f))
            #self.start_urls.append(url)
            #self.brief_ids.append(publisherId + productId)


  def parseSearch(self, response, id, filename):
    sel = Selector(response)
    found_list = sel.xpath('//p[@class="tmb"]')
    if len(found_list) > 0:
      found = found_list[0]
      #for found in found_list:
      link_list = found.xpath('a/@href').extract()
      for link in link_list:
        print link
        print filename
        yield Request(link, cookies={'cklg': 'ja'}, meta={'dont_merge_cookies': True}, callback=lambda r, id=id,filename=filename:self.parseDetail(r,id,filename))

  def parseDetail(self, response, id, filename):
    sel = Selector(response)
    items = []
    print filename
    item = DmmQueryItem()
    item['filename'] = filename
    item['directory'] = self.directory
    item['actress'] = "---"
    item['link'] = response.url
    item['cover'] = sel.xpath('//a[@name="package-image"]/@href').extract()[0]
    actress_list = sel.xpath('//span[@id="performer"]/a/text()').extract()
    for actress in actress_list:
      item['actress'] = actress

    item['title'] = sel.xpath('//h1[@id="title"]/text()').extract()[0]
    item['productDmmId'] = sel.xpath(u'//table[@class="mg-b20"]/tr/td[contains(text(),"品番：")]/following-sibling::td/text()').extract()[0]
    item['productId'] = id
    thumbnail_list = sel.xpath('//div[@id="sample-image-block"]/a/img/@src').extract()
    thumbnail_large_list = []
    for thumbnail in thumbnail_list:
      thumbnail_large = thumbnail.replace('-', 'jp-')
      thumbnail_large_list.append(thumbnail_large)

    item['thumbnails'] = thumbnail_large_list

    print item['cover']
    print item['actress']
    print item['title']
    print item['productId']
    print item['link']
    print item['thumbnails']
    items.append(item)
    return items

