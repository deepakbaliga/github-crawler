# -*- coding: utf-8 -*-
import scrapy
import time
import json
import pprint
from neo4j.v1 import GraphDatabase, basic_auth


class GithubfollowersSpider(scrapy.Spider):

    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "janaganamana"))


    name = "githubfollowers"
    allowed_domains = ["https://github.com/"]
    start_urls = ['https://github.com/JakeWharton?tab=followers']
    handle_httpstatus_list = [429]


    #This function will parse individual profile lines
    #remember just the profile links but doesnt scrap the profile itself.
    def parse_body(self, response):
        print "\t\t######################################################"
        print "\t\tParsing the followers list for "+response.url
        print "\t\t######################################################"
        for item in response.xpath('//div[@class="js-repo-filter position-relative"]/div/div[1]/a/@href'):
            yield scrapy.Request('https://github.com'+item.extract(), callback=self.parse_profile, dont_filter=True)
        return


    def parse(self, response):

        print "----------------------------------------------------"
        print "Now Parsing : " +  response.url
        print "----------------------------------------------------"

        item = {}



        if response.status == 429:
            print "\n\n WAITING FOR 2 MINUTES (Under parse - githubfollowers.py) \n\n"
            time.sleep(120)
            yield scrapy.Request(response.url, callback=self.parse,dont_filter=True)
            return

        yield scrapy.Request(response.url, callback=self.parse_body, dont_filter=True)

        try:
            text = response.xpath('//div[@class="pagination"]/a/text()')[0].extract()
        except Exception:
            print "Only one page found"
            return

        length = len(response.xpath('//div[@class="pagination"]/a/text()'))
        nextUrl = ""

        if text == "Next" and length == 1:
            nextUrl =  response.xpath('//div[@class="pagination"]/a/@href')[0].extract()
        elif text == "Previous" and length == 1:
            nextUrl = None
        else:
            nextUrl = response.xpath('//div[@class="pagination"]/a[2]/@href')[0].extract()



        if not nextUrl == None:
            yield scrapy.Request(nextUrl, callback=self.parse,dont_filter=True)


    ####### Neo4J things ########
    def query_database(self, query):
        session = this.driver.session()
        ## Write your query here
        session.close()

    def check_if_exists(self, username):

        session = self.driver.session()
        result = session.run("MATCH (a:user) WHERE a.username = '"+username+"' RETURN a")
        session.close()

        for record in result:
            return True

        return False

    def insert_user(self, user):
        session = self.driver.session()
        user_string = 'username : "'+user['username']+'", full_name : "'+user['full_name']+'", image_url : "'+user['image_url']+'", city : "'+user['city']+'", joined_on : "'+user['joined_on']+'", email : "'+user['email']+'", bio : "'+user['bio']+'", website : "'+user['website']+'"'
        session.run("CREATE (user_node:user { "+user_string+" })")
        session.close()


    def parse_profile(self,response):

        print "-----------------------------------------"
        print "Scrapping : "+ response.url
        print "-----------------------------------------"
        item = {}

        try:
            item['email'] = response.xpath('//li[@aria-label="Email"]/a/text()')[0].extract().lstrip('\n').lstrip(' ').rstrip('\n')
        except Exception:
            print "Email Doesnt exist"
            item['email'] = "null";


        try:
            item['website'] = response.xpath('//li[@aria-label="Blog or website"]/a/text()')[0].extract().lstrip('\n').lstrip(' ').rstrip('\n')
        except Exception:
            print "Website Doesnt exist"
            item['website'] = "null";

        try:
            item['bio'] = response.xpath('//*[@id="js-pjax-container"]/div/div[1]/div[3]/div/text()')[0].extract().lstrip('\n').lstrip(' ').rstrip('\n')
        except Exception:
            print "Bio doesnt exist"
            item['bio'] = "null";


        try:
            item['joined_on'] = response.xpath('//local-time[@class="join-date"]/text()')[0].extract().lstrip('\n').lstrip(' ').rstrip('\n').rstrip(' ').rstrip('\n')
        except Exception:
            print "Joined date doesnt exist"
            item['joined_on'] = "null";

        try:
            item['city'] = response.xpath('//li[@aria-label="Home location"]/text()')[0].extract().lstrip('\n').lstrip(' ').rstrip('\n')
        except Exception:
            print "City isnt mentioned"
            item['city'] = "null";

        try:
            item['image_url'] = response.xpath('/html/body/div[@role="main"]/div[@id="js-pjax-container"]/div/div[1]/a[1]/@href')[0].extract().lstrip('\n').lstrip(' ').rstrip('\n').lstrip('https://')
        except Exception:
            print "No profile picture image"
            item['image_url'] = "null";

        try:
            item['full_name'] = response.xpath('//div[@class="vcard-names-container py-3 js-sticky js-user-profile-sticky-fields "]/h1[@class="vcard-names"]/span[1]/text()')[0].extract()
        except Exception:
            print "No profile picture image"
            item['full_name'] = "null";


        try:
            item['username'] = response.xpath('//div[@class="vcard-names-container py-3 js-sticky js-user-profile-sticky-fields "]/h1[@class="vcard-names"]/span[2]/text()')[0].extract()
        except Exception:
            print "No profile picture image"
            item['username'] = "null";



        self.print_table(item)

        if self.check_if_exists(item['username']) == False:
            self.insert_user(item)


    def parse_link(self, response):
        print response.url
