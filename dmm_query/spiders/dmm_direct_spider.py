# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.selector import Selector
from dmm_query.items import DmmQueryItem
from scrapy.http import Request

class DmmDirectSpider(Spider):
  name = "DmmDirect"
  allowed_domains = ["dmm.co.jp"]
  start_url_template = "http://www.dmm.co.jp/search/=/searchstr=%s%%20%s/n1=FgRCTw9VBA4GAVhfWkIHWw__/n2=Aw1fVhQKX1ZRAlhMUlo5QQgBU1lR/"
  start_urls = [
    "http://www.dmm.co.jp/search/=/searchstr=rbd%20550/n1=FgRCTw9VBA4GAVhfWkIHWw__/n2=Aw1fVhQKX1ZRAlhMUlo5QQgBU1lR/"
  ]
  directory = "/home/pi/dmm_query/dest"

  def __init__(self, url, directory=None, *args, **kwargs):
    super(DmmDirectSpider, self).__init__(*args, **kwargs)
    if url != None:
      self.start_urls = [url]
    if directory != None:
      self.directory = directory

  def parse(self, response):
    sel = Selector(response)
    items = []
    item = DmmQueryItem()
    item['directory'] = self.directory
    item['filename'] = "_NonExists"    
    item['link'] = response.url
    item['actress'] = "---"
    item['cover'] = sel.xpath('//a[@name="package-image"]/@href').extract()[0]
    actress_list = sel.xpath('//span[@id="performer"]/a/text()').extract()
    for actress in actress_list:
      item['actress'] = actress

    item['title'] = sel.xpath('//h1[@id="title"]/text()').extract()[0]
    item['productId'] = sel.xpath(u'//table[@class="mg-b20"]/tr/td[contains(text(),"品番：")]/following-sibling::td/text()').extract()[0]
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

