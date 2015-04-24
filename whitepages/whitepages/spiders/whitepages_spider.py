from scrapy.http import FormRequest
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import string
import html2text

from whitepages.items import WhitepagesItem



class WhitePagesSpider(CrawlSpider):
    name = 'whitepages'
    allowed_domains = ['whitepages.tufts.edu']
    rules = (
        Rule(LinkExtractor(allow=('ldapentry\.cgi',)), callback='parse_item'),
    )

    def start_requests(self):
        searches = [a+b+c for a in string.lowercase
                          for b in string.lowercase
                          for c in string.lowercase]
        formdata = {'x': '0',
                    'y': '0',
                    'type': '+',
                    'search': 'aa'
                    }
        requests = []
        for search in searches:
            formdata['search'] = search
            fr = FormRequest("http://whitepages.tufts.edu/searchresults.cgi",
                             formdata=formdata, callback=self.parse)
            requests.append(fr)

        return requests


    def parse_item(self, response):
         # from scrapy.shell import inspect_response
         # inspect_response(response)

        wpi = WhitepagesItem()
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        class_year = response.xpath(".//b[text()='Class Year: ']/../../following-sibling::td[1]").extract()

        if len(class_year) != 1:
            return None

        class_year = converter.handle(class_year[0]).strip()
        if class_year != "15":
            return None

        name = response.xpath(".//b[text()='Name: ']/../../following-sibling::td[1]").extract()
        if len(name) != 1:
            return None

        wpi['name'] = converter.handle(name[0]).replace('|', '').strip()

        major = response.xpath(".//b[text()='Major: ']/../../following-sibling::td[1]").extract()
        if len(major) != 1:
            wpi['major'] = None
        else:
            wpi['major'] = converter.handle(major[0]).replace('|', '').strip()


        for url in response.xpath('//a/@href'):
            link = url.extract()
            if link.startswith('mailto:'):
                wpi['email'] = link.replace('mailto:', '')
        wpi['class_year'] = class_year

        return wpi
