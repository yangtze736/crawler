# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from douban.items import DoubanItem

class Douban(CrawlSpider):
	name = "douban"
	redis_key = 'douban:start_urls'
	start_urls = ['http://movie.douban.com/top250']

	url = 'http://movie.douban.com/top250'

	def parse(self,response):
		#print response.body
		item = DoubanItem()
		selector = Selector(response)
		Movies = selector.xpath('//div[@class="info"]')
		for eachMovie in Movies:
			title = eachMovie.xpath('div[@class="hd"]/a/span/text()').extract()
			fullTitle = ''
			for each in title:
				fullTitle += each
			movieInfo = eachMovie.xpath('div[@class="bd"]/p/text()').extract()
			star = eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
			quote = eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
			#quote可能为空，需要先进行判断
			if quote:
				quote = quote[0]
			else:
				quote = ''
			item['title'] = fullTitle
			item['movieInfo'] = ';'.join(movieInfo)
			item['star'] = star
			item['quote'] = quote
			yield item
		nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
		#第十页是最后一页，没有下一页的链接
		if nextLink:
			nextLink = nextLink[0]
			#print nextLink
			yield Request(self.url + nextLink,callback=self.parse)

