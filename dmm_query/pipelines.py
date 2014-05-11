# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
from subprocess import call

class JsonWriterPipeline(object):
  def process_item(self, item, spider):
    filename = item['productId']
    file = open(filename + ".json", 'wb')
    text = json.dumps(dict(item))
    file.write(text)
    return item

class FinalizerPipeline(object):
  def process_item(self, item, spider):
    productId = item['productId']
    filename = productId + ".json"
    directoryPrefix = item['directory']
    movieFilename = directoryPrefix + '/' + item['filename']
    actress = item['actress']
    title = item['title']
    directory = directoryPrefix + '/' + actress + u'/[' + productId + u']' + title
    call(['mv', filename, directory])
    call(['mv', movieFilename, directory])
    return item

class ContentCreatorPipeline(object):
  def process_item(self, item, spider):
    directoryPrefix = item['directory']
    cover = item['cover']
    actress = item['actress']
    productId = item['productId']
    title = item['title']
    thumbnailList = item['thumbnails']
    directory = directoryPrefix + '/' + actress + u'/[' + productId + u']' + title
    print "Creating directory for [" + productId + "]: " + directory
    call(["mkdir", actress])
    call(["mkdir", directory])
    print "Fetching cover..."
    call(['wget', cover, "-N", "--directory-prefix=" + directory])
    print "Fetching thumbnails..."
    num = 1
    for thumbnail in thumbnailList:
      print "Fetching " + str(num) + "..."
      num = num + 1
      call(['wget', thumbnail, "-N", "--directory-prefix=" + directory])

    return item
    

