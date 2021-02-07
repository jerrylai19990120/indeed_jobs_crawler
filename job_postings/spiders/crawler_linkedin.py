import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from shutil import which
import time

class CrawlerLinkedinSpider(scrapy.Spider):
    name = 'crawler_linkedin'
    allowed_domains = ['www.linkedin.com']
    start_urls = ['http://www.linkedin.com/']

    def __init__(self):
        options = Options()
        options.add_argument('--headless')

        chrome_path = which("../selenium_basics/chromedriver.exe")
        self.driver = webdriver.Chrome(executable_path=chrome_path)


    def parse(self, response):
        
        for i in range(0, 500, 25):
            self.driver.get(f'https://www.linkedin.com/jobs/search/?geoId=101174742&keywords=software%20engineer&location=Canada&start={i}')
            time.sleep(3)
            html = self.driver.page_source
            resp = Selector(text=html)

            jobs = resp.xpath('//div[@class="flex-grow-1 artdeco-entity-lockup artdeco-entity-lockup--size-4 ember-view"]')

            for job in jobs:
                yield {
                    "job title": job.xpath('.//a[@class="disabled ember-view job-card-container__link job-card-list__title"]/text()').get(),
                    "company": job.xpath('.//a[@data-control-name="job_card_company_link"]/text()').get(),
                    "location": job.xpath('.//li[@class="job-card-container__metadata-item"][1]/text()').get()
                }

