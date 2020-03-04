# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TuItem(scrapy.Item):
	
	name = scrapy.Field()
	location = scrapy.Field()
	price = scrapy.Field()
	# rating
	star = scrapy.Field()
	rating = scrapy.Field() 
	cleanliness_rating = scrapy.Field()
	service_staff_rating = scrapy.Field()
	amentities_rating = scrapy.Field()
	prorerty_condition_rating = scrapy.Field()
	# the numbers of reviews 
	reviews_num = scrapy.Field()
	excellent_num = scrapy.Field()
	good_num = scrapy.Field()
	okay_num = scrapy.Field()
	mediocre_num = scrapy.Field()
	poor_num = scrapy.Field()
	#link
	link = scrapy.Field()



