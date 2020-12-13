import scrapy
from scrapy.loader import ItemLoader
from wg.items import WgItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    # start_urls = ['http://douban.com/']

    # def parse(self, response):
    #     pass

    def start_requests(self):
        # yield scrapy.Request('http://www.example.com/1.html', self.parse)
        # yield scrapy.Request('http://www.example.com/2.html', self.parse)
        # yield scrapy.Request('http://www.example.com/3.html', self.parse)

        for page_no in range(0,200,20):
            # yield scrapy.Request('https://movie.douban.com/subject/26957989/comments?start=%d&limit=20&status=P&sort=new_score' % (page_no), self.parse_thread_list)
            # yield scrapy.Request('https://movie.douban.com/subject/26957989/comments?start=%d&limit=20&status=P&sort=time' % (page_no), self.parse_thread_list)
            yield scrapy.Request('https://movie.douban.com/subject/2154349/comments?start=%d&limit=20&status=P&sort=time' % (page_no), self.parse_thread_list)

    def parse_thread_list(self, response):
        # url = response.xpath('//body/div[@id="wrapA"]/div/div/table/tbody/tr/td/h3/a[contains(@href, "htm_data")]/@href').getall()[1:5]
        # url = response.xpath('//body/div[@id="wrapA"]/div/div/table/tbody/tr/td/h3/a[contains(@href, "htm_data")]/@href').getall()
        # self.logger.info('url %s', url)

        self.logger.info('Parse function called on %s', response.url)
        # self.logger.info('response %s', response)
        # if response.status_code!=200:
        #     return

        # self.logger.info('user_name: ', response.xpath('/html/body/div[@id="wrapper"]/div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/div[@id="comments"]/div[@class="comment-item "]/div[@class="comment"]/h3/span[@class="comment-info"]/a/text()').getall()[1:3])
        # self.logger.info('comment_rating: ', response.xpath('/html/body/div[@id="wrapper"]/div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/div[@id="comments"]/div[@class="comment-item "]/div[@class="comment"]/h3/span[@class="comment-info"]/span[2]/@class'))

        thread_item = ItemLoader(item=WgItem(), response=response)
        thread_item.add_xpath('user_name', '/html/body/div[@id="wrapper"]/div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/div[@id="comments"]/div[@class="comment-item "]/div[@class="comment"]/h3/span[@class="comment-info"]/a/text()')
        # xpath = '/html/body/div[@id="wrapper"]/div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/div[@id="comments"]/div[@class="comment-item "]/div[@class="comment"]/h3/span[@class="comment-info"]/a/text()'
        # user_names = self.get_array_by_xpath(xpath, response)
        # thread_item.add_value('user_name', user_names)

        # thread_item.add_xpath('comment_rating', '/html/body/div[@id="wrapper"]/div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/div[@id="comments"]/div[@class="comment-item "]/div[@class="comment"]/h3/span[@class="comment-info"]/span[contains(@class, "rating")]/@class')
        # print(list(map(lambda x: x ** 2, lst1)))  # 使用 lambda 匿名函数
        # print(list(map(lambda x,y: x+y, lst2,lst3)))  # 使用 lambda 匿名函数
        # comment_rating = response.xpath('/html/body/div[@id="wrapper"]/div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/div[@id="comments"]/div[@class="comment-item "]/div[@class="comment"]/h3/span[@class="comment-info"]/span[contains(@class, "rating")]/@class').getall()
        comment_rating = response.xpath('/html/body/div[@id="wrapper"]/div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/div[@id="comments"]/div[@class="comment-item "]/div[@class="comment"]/h3/span[@class="comment-info"]/span[2]/@class').getall()
        comment_rating = list(map(lambda x: x[7:9] if x[7:9].isdigit() else 0, comment_rating))
        thread_item.add_value('comment_rating', comment_rating)

        # thread_item.add_xpath('comment_date', '/html/body/div[@id="wrapper"]/div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/div[@id="comments"]/div[@class="comment-item "]/div[@class="comment"]/h3/span[@class="comment-info"]/span[contains(@class, "comment-time ")]/text()')
        comment_date = response.xpath('/html/body/div[@id="wrapper"]/div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/div[@id="comments"]/div[@class="comment-item "]/div[@class="comment"]/h3/span[@class="comment-info"]/span[contains(@class, "comment-time ")]/text()').getall()
        comment_date = list(map(lambda x: x.replace("\n","").strip(), comment_date))
        thread_item.add_value('comment_date', comment_date)

        # thread_item.add_xpath('comment_content', '/html/body/div[@id="wrapper"]/div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/div[@id="comments"]/div[@class="comment-item "]/div[@class="comment"]/p[@class=" comment-content"]/span[@class="short"]/text()')
        # xpath = '/html/body/div[@id="wrapper"]/div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/div[@id="comments"]/div[@class="comment-item "]/div[@class="comment"]/p[@class=" comment-content"]/span[@class="short"]'
        # comment_content = self.get_array_by_xpath(xpath, response)
        # thread_item.add_value('comment_content', comment_content)
        comment_content = response.xpath('/html/body/div[@id="wrapper"]/div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/div[@id="comments"]/div[@class="comment-item "]/div[@class="comment"]/p[@class=" comment-content"]/span[@class="short"]')
        comment_content = list(map(lambda x: '' if x.xpath('text()').get()==None else str(x.xpath('text()').get()), comment_content))
        thread_item.add_value('comment_content', comment_content)

        # return response.follow_all(url, self.parse_thread)
        return thread_item.load_item()

    # def get_array_by_xpath(self, xpath, response):
    #     arr = response.xpath(xpath).getall()
    #     x=[]
    #     for c in arr:
    #         x.append('' if c.text==None else c.text)
    #     print(x)
    #     return x
