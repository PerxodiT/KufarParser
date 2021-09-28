import requests
import Config
from bs4 import BeautifulSoup, Tag
from lxml import etree


class PageLoader:
    def __init__(self, page):
        self.Session = requests.session()
        self.Session.headers = Config.HEADERS
        self.Page = page
        self.PageNum = 1

    def isNextPageExist(self, dom) -> bool:
        #                  //*[@id="listings_content"]/div[1]/div/div[10]/div/a[5]
        items = dom.xpath('//*[@id="listings_content"]/div[1]/div/div[10]/div/a[last()]')
        return len(items[0].get('class').split()) > 1

    def getNextPageURL(self, dom) -> str:
        return 'https://auto.kufar.by' + dom.xpath('//*[@id="listings_content"]/div[1]/div/div[10]/div/a[last()]')[0].get('href')

    def getCarLinks(self) -> list:
        links = []
        bs = BeautifulSoup(self.Session.get(self.Page).text, 'html.parser')
        dom = etree.HTML(str(bs))
        page = 1
        while (self.isNextPageExist(dom)):
            print(f"Parsing page {page}")
            page += 1
            bs = BeautifulSoup(self.Session.get(self.Page).text, 'html.parser')
            dom = etree.HTML(str(bs))
            items = dom.xpath('//*[@id="listings_content"]/div[1]/div/div[9]/article/div/a')
            for i in items:
                links.append(i.get('href'))
            self.Page = self.getNextPageURL(dom)
        return links[::-1]



# //*[@id="listings_content"]/div[1]/div/div[10]/div/a[4]


if __name__ == '__main__':
    pl = PageLoader(Config.LINK)#"""https://auto.kufar.by/listings?crg=2&cur=USD&prc=r%3A0%2C500&rgn=6&sort=lst.d&cat=2010&cursor=eyJ0IjoiYWJzIiwiZiI6ZmFsc2UsInAiOjF9""")
    pl.getCarLinks()