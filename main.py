from scrapy.cmdline import execute
from novel_spider.settings import ROOT_PATH
import sys

sys.path.extend(ROOT_PATH)

if __name__ == '__main__':
    execute(["scrapy", "crawl", "biquge"])
# "-s", "JOBDIR=spider_info/qidian"