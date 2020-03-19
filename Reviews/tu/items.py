# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TuItem(scrapy.Item):
	hotel_name = scrapy.Field()
	usr_name = scrapy.Field()
	rating = scrapy.Field()
	liked = scrapy.Field()
	review_date = scrapy.Field()
	stay_duration = scrapy.Field() 
	review = scrapy.Field()
	response = scrapy.Field()



