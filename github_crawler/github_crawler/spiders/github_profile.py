# -*- coding: utf-8 -*-
import scrapy
import json
from tabulate import tabulate

class GithubProfileSpider(scrapy.Spider):
    name = "github_profile"
    allowed_domains = ["https://github.com/"]
    start_urls = ['https://github.com/deepakbaliga','https://github.com/bolimit']

    def print_table(self,data):
        print json.dumps(data)



    def parse(self,response):

        item = {}

        try:
            item['email'] = response.xpath('//li[@aria-label="Email"]/a/text()')[0].extract().lstrip('\n').lstrip(' ').rstrip('\n')
        except Exception:
            #print "Email Doesnt exist"
            item['email'] = None;


        try:
            item['website'] = response.xpath('//li[@aria-label="Blog or website"]/a/text()')[0].extract().lstrip('\n').lstrip(' ').rstrip('\n')
        except Exception:
            #print "Website Doesnt exist"
            item['website'] = None;

        try:
            item['bio'] = response.xpath('//*[@id="js-pjax-container"]/div/div[1]/div[3]/div/text()')[0].extract().lstrip('\n').lstrip(' ').rstrip('\n')
        except Exception:
            #print "Bio doesnt exist"
            item['bio'] = None;


        try:
            item['joined_on'] = response.xpath('//local-time[@class="join-date"]/text()')[0].extract().lstrip('\n').lstrip(' ').rstrip('\n').rstrip(' ').rstrip('\n')
        except Exception:
            #print "Joined date doesnt exist"
            item['joined_on'] = None;

        try:
            item['city'] = response.xpath('//li[@aria-label="Home location"]/text()')[0].extract().lstrip('\n').lstrip(' ').rstrip('\n')
        except Exception:
            #print "City isnt mentioned"
            item['city'] = None;

        try:
            item['image_url'] = response.xpath('/html/body/div[@role="main"]/div[@id="js-pjax-container"]/div/div[1]/a[1]/@href')[0].extract().lstrip('\n').lstrip(' ').rstrip('\n')
        except Exception:
            #print "No profile picture image"
            item['image_url'] = None;

        try:
            item['full_name'] = response.xpath('//div[@class="vcard-names-container py-3 js-sticky js-user-profile-sticky-fields "]/h1[@class="vcard-names"]/span[1]/text()')[0].extract()
        except Exception:
            #print "No profile picture image"
            item['full_name'] = None;


        try:
            item['username'] = response.xpath('//div[@class="vcard-names-container py-3 js-sticky js-user-profile-sticky-fields "]/h1[@class="vcard-names"]/span[2]/text()')[0].extract()
        except Exception:
            #print "No profile picture image"
            item['username'] = None;

        self.print_table(item)
        yield scrapy.Request("https://github.com/deepakbaliga", callback = self.parse_link,dont_filter=True)



    def parse_link(self, response):
        print response.url
