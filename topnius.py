import sys
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class TopEnginyeriaSpider(Spider):

    def __init__(self, start=0, end=0):
        dispatcher.connect(self.spider_closed, signals.spider_closed) #to catch the spider finalization signal
        self.found=0
        
        self.start_urls=[]        
        for niu in range(start, (end+1)): #adding in a list all custom urls inside the range
            self.start_urls.append('http://deic-projectes.uab.cat/gamification/perfil.php?niu=%s' % niu)

        self.file = open("TopNius_"+str(start)+"-"+str(end)+".txt","w")
        self.file.write('NIU	Nom\n')


    def parse(self, response):
        sel = Selector(response)
        entry=  sel.xpath("//div[@class='col-md-5 column']/h2/text()")
        newNIU = str(response)[63:70]
        badname = entry.extract()
        
        data = '| ' + newNIU + ' | ' + badname[0].strip() + ' |\n'
        self.file.write(data)

        self.found+=1


    def spider_closed(self, spider):
        self.file.close()
        print('FOUND ' + str(self.found) + ' NIUS.')


        
if __name__ == "__main__":
    if int(len(sys.argv)) == 3:
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'DOWNLOAD_DELAY': 1, #this value defines the delay between 2 requests
            'RANDOMIZE_DOWNLOAD_DELAY': True, #enables random delay between 0.5*DOWNLOAD_DELAY and 1.5*DOWNLOAD_DELAY
            'REDIRECT_MAX_TIMES':0,
            'ROBOTSTXT_OBEY': True,
            #'CONCURRENT_REQUESTS_PER_IP': 1
            #'AUTOTHROTTLE_ENABLED': True,
            #'AUTOTHROTTLE_START_DELAY': 1,
            #'AUTOTHROTTLE_MAX_DELAY': 10
        })
        startPoint = int(sys.argv[1])
        endPoint = int(sys.argv[2])
        process.crawl(TopEnginyeriaSpider, start=startPoint, end=endPoint)
        process.start()
    else:
        print(len(sys.argv), "Incorrect arguments. Must be 2. E.g: python main.py 1461130 1461150")
