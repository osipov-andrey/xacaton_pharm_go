from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Initialize the CrawlerProcess
process = CrawlerProcess(get_project_settings())

# Get the list of all available spiders
spider_list = process.spider_loader.list()

# Run each spider
for spider_name in spider_list:
    process.crawl(spider_name)

# Start the crawling process
process.start()
