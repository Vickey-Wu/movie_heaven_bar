# -*- coding: utf-8 -*-
import scrapy
import hashlib
import time
import logging
from scrapy.http import Request
from movie_heaven_bar.items import MovieHeavenBarItem
from scrapy_redis.spiders import RedisSpider


class NewestMovieSpider(scrapy.Spider):
    name = 'newest_movie'
    allowed_domains = ['www.dytt8.net']
    #start_urls = ['http://www.dytt8.net/']
    # 从该urls列表开始爬取
    start_urls = ['http://www.dytt8.net/html/gndy/dyzz/']

    def get_hash(self, data):
        md5 = hashlib.md5()
        md5.update(data.encode('utf-8'))
        return md5.hexdigest()

    def parse(self, response):
        item = MovieHeavenBarItem()
        domain = "https://www.dytt8.net"

        # 爬取下一页
        last_page_num = response.xpath('//select[@name="sldd"]//option[last()]/text()').extract()[0]
        last_page_url = 'list_23_' + last_page_num + '.html'
        next_page_url = response.xpath('//div[@class="x"]//a[last() - 1]/@href').extract()[0]
        next_page_num = next_page_url.split('_')[-1].split('.')[0]
        if next_page_url != last_page_url:
            url = 'https://www.dytt8.net/html/gndy/dyzz/' + next_page_url
            logging.log(logging.INFO, f'***************** crawling page {next_page_num} ***************** ')
            yield Request(url=url, callback=self.parse, meta={'item': item}, dont_filter = True)

        # 爬取详情页
        urls = response.xpath('//b/a/@href').extract()     # list type
        #print('urls', urls)
        for url in urls:
            url = domain + url
            yield Request(url=url, callback=self.parse_single_page, meta={'item': item}, dont_filter = False)

    def parse_single_page(self, response):
        item = response.meta['item']
        item['movie_link'] = response.url
        logging.log(logging.INFO, 'crawling url: ' + item['movie_link'])
        detail_row = response.xpath('//*[@id="Zoom"]//p/text()').extract()		# str type list
        # 将网页提取的str列表类型数据转成一个长字符串, 以圆圈为分隔符，精确提取各个字段具体内容
        detail_str = ''.join(detail_row)
        # 将电影详细内容hash，以过滤相同内容
        item['movie_hash'] = self.get_hash(detail_str)
        logging.log(logging.INFO, f"movie hash is: {item['movie_hash']}")
        detail_list = ''.join(detail_str).split('◎')

        logging.log(logging.INFO, '**************** movie detail log ****************')
        item['movie_name'] = detail_list[1][5:].replace(6*u'\u3000', u', ')
        logging.log(logging.INFO, 'movie_link: ' + item['movie_link'])
        logging.log(logging.INFO, 'movie_name: ' + item['movie_name'])
        # 找到包含特定字符到字段
        for field in detail_list:
            if '主\u3000\u3000演' in field:
                # 将字段包含杂质去掉[5:].replace(6*u'\u3000', u', ')
                item['movie_actors'] = field[5:].replace(6*u'\u3000', u', ')
                logging.log(logging.INFO, 'movie_actors: ' + item['movie_actors'])
            if '导\u3000\u3000演' in field:
                item['movie_director'] = field[5:].replace(6*u'\u3000', u', ')
                logging.log(logging.INFO, 'movie_directors: ' + item['movie_director'])
            if '上映日期' in field:
                item['movie_publish_date'] = field[5:].replace(6*u'\u3000', u', ')
                logging.log(logging.INFO, 'movie_publish_date: ' + item['movie_publish_date'])
            if '豆瓣评分' in field:
                item['movie_score'] = field[5:].replace(6*u'\u3000', u', ')
                logging.log(logging.INFO, 'movie_score: ' + item['movie_score'])

        # 此处获取的是迅雷磁力链接，安装好迅雷，复制该链接到浏览器地址栏迅雷会自动打开下载链接，个别网页结构不一致会获取不到链接
        try:
            item['movie_download_link'] = ''.join(response.xpath('//p/a/@href').extract())
            logging.log(logging.INFO, 'movie_download_link: ' + item['movie_download_link'])
        except Exception as e:
            item['movie_download_link'] = response.url
            logging.log(logging.WARNING, e)
        yield item
