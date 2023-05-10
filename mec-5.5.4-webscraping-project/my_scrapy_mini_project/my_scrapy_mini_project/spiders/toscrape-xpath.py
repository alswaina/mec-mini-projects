import scrapy
from urllib.parse import urlparse


class QuoteToDict(scrapy.Spider):
    name = 'toscrape-xpath'

    start_urls = ['http://quotes.toscrape.com/']
    page = 1

    def parse(self, response):
        server = urlparse(response.url)
        server = server.scheme + "://" + server.hostname

        quotes = response.xpath("/html/body/div[1]/div[2]/div[1]/div")

        for quote in quotes:
            response.xpath(
                "/html/body/div[1]/div[2]/div[1]/div[1]/span[1]/text()").get()
            yield {
                'quote': quote.xpath("span[1]/text()").get(),
                'author': quotes.xpath("span[2]/small/text()").get(),
                'about': server + quotes.xpath("span[2]/a/@href").get(),
                'tags': quote.xpath("div/meta/@content").get()
            }
        self.page += 1
        # response.xpath("/html/body/div[1]/div[2]/div[1]/nav/ul/li/a/@href").get()
        post_links = response.xpath(
            "/html/body/div[1]/div[2]/div[1]/nav/ul/li/a")
        if len(post_links) == 1:
            # there is on link: next or previous
            next_page = server + \
                post_links[0].xpath("@href").get()
        elif len(post_links) > 1:
            # there are more than one link: next and previous
            next_page = server + \
                post_links[1].xpath("@href").get()
        else:
            print('No next page!')
        print(f"expecting page = {self.page}")
        print(f"next page is {next_page}")
        if next_page is not None and next_page.split('/')[-2] == str(self.page):
            print(f"calling {next_page}")
            yield response.follow(next_page, callback=self.parse)
