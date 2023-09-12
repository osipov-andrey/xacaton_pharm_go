from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    process = CrawlerProcess(get_project_settings())
    spider_list = process.spider_loader.list()

    for spider_name in spider_list:
        process.crawl(spider_name)

    # Start the crawling process
    process.start()


if __name__ == '__main__':
    main()
