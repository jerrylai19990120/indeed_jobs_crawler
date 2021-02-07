from enum import Flag
from os import close, confstr
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from selenium.webdriver.common.keys import Keys
from shutil import which
import time

class MarketingJobsSpider(scrapy.Spider):
    name = 'jobs_crawler'
    allowed_domains = ['ca.indeed.com']
    start_urls = ['https://ca.indeed.com/']

    def __init__(self):

        options = Options()
        options.add_argument('--headless')

        chrome_path = which("../selenium_basics/chromedriver.exe")

        self.driver = webdriver.Chrome(executable_path=chrome_path, options=options)
    


    def parse(self, response):

        for i in range(0, 500, 10):
            self.driver.get(f'https://ca.indeed.com/jobs?q=software-engineer&l=Mississauga,+ON&start={i}')
            time.sleep(3)
            html = self.driver.page_source
            resp = Selector(text=html)
            postings = resp.xpath('//div[@class="jobsearch-SerpJobCard unifiedRow row result clickcard"]')
            separator = " "
            for posting in postings:
                yield {
                    "job title": separator.join(posting.xpath('.//h2[@class="title"]/descendant::*/text()').getall()).strip('\n'),
                    "company": posting.xpath('normalize-space(.//span[@class="company"]/a/text())').get(),
                    "location": posting.xpath('normalize-space(.//div[@class="location accessible-contrast-color-location"]/text())').get(),
                    "salary": posting.xpath('normalize-space(.//span[@class="salaryText"]/text())').get(),
                }
            