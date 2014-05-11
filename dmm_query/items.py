# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class DmmQueryItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    link = Field()
    cover = Field()
    thumbnails = Field()
    actress = Field()
    productId = Field()
    productDmmId = Field()
    filename = Field()
    directory = Field()

