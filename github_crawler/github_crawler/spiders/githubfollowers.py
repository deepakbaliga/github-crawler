# -*- coding: utf-8 -*-
import scrapy


class GithubfollowersSpider(scrapy.Spider):
    name = "githubfollowers"
    allowed_domains = ["github.com/deepakbaliga/followers"]
    start_urls = ['http://github.com/deepakbaliga/followers/']

    

    def parse(self, response):
        pass
