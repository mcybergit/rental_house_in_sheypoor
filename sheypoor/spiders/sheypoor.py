import scrapy
import re


def changenumber(text):
    n=0
    pn = ('۰','۱','۲','۳','۴','۵','۶','۷','۸','۹',)

    for i in pn:

        text = text.replace(i,str(n))
        n+=1
    text = text.replace(',','')
    return text

def Price_rent(text):
    rent=0



def Price(text):
    rent=0
    mortgage=0
    p=re.findall('<p.*?</p', text)
    if len(p)> 0:

        for i in range(len(p)):
            if 'رهن:' in p[i]:
                mortgage=(int(re.findall('(\d+)', p[i])[0]))
            if 'اجاره:' in p[i]:
                rent=(int(re.findall('(\d+)', p[i])[0]))
    return (rent,mortgage)



class SheypoorSpider(scrapy.Spider):
    name = "sheypoor"
    start_urls = [
    # insert your distenation link
        'https://www.sheypoor.com/%D8%AA%D9%87%D8%B1%D8%A7%D9%86/%D9%86%DB%8C%D8%B1%D9%88%DB%8C-%D9%87%D9%88%D8%A7%DB%8C%DB%8C/%D8%A7%D9%85%D9%84%D8%A7%DA%A9/%D8%B1%D9%87%D9%86-%D8%A7%D8%AC%D8%A7%D8%B1%D9%87-%D8%AE%D8%A7%D9%86%D9%87-%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86',
    ]

    def parse(self, response):
        for case in response.css('#serp .list'):
            edit = changenumber(case.css('.to-bottom').get())
            price = Price(edit)
            if price[0]*100/3 + price[1] <= 1000000000 and price[0] + price[1]>200000000:

                yield {
                    'title': case.css('a::text').getall()[-1],
                    'locations':re.findall('>\s+(.+)\s+', case.css('p').getall()[1])[0][7:],
                    'time':case.css('time::text').get(),
                    'mortgage': price[1],
                    'rent': price[0],
                    'link': case.css('a::attr(href)').get(),
                }

        next_page = response.css('.next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
