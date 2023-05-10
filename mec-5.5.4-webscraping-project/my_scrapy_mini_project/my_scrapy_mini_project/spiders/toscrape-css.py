import scrapy
from urllib.parse import urlparse


class QuoteToDict(scrapy.Spider):
    name = 'toscrape-css'

    start_urls = ['http://quotes.toscrape.com/']
    page = 1

    def parse(self, response):
        server = urlparse(response.url)
        server = server.scheme + "://" + server.hostname

        quotes = response.css('div.quote')

        for quote in quotes:
            yield {
                'quote': quote.css('span::text').get(),
                'author': quote.css('small.author::text').get(),
                'about': server + quote.css('a').attrib['href'],
                'tags': quote.css('meta.keywords').attrib['content']
            }
        self.page += 1

        post_links = response.css('nav')[0].css('a')
        if len(post_links) == 1:
            # there is on link: next or previous
            next_page = server + \
                post_links[0].attrib['href']
        elif len(post_links) > 1:
            # there are more than one link: next and previous
            next_page = server + \
                post_links[1].attrib['href']
        else:
            print('No next page!')

        if next_page is not None and next_page.split('/')[-2] == str(self.page):
            # when next_page is equal to next expected page i.e. self.page counter
            yield response.follow(next_page, callback=self.parse)
