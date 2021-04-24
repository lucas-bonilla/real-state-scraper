# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import re

class PisoscomSpider(scrapy.Spider):
    name = 'pisoscom_casas'
    allowed_domains = ['pisos.com']
    # start_urls = ['https://www.pisos.com/venta/casas-benalmadena/%s' % page for page in range(1,3)]
    start_urls = ['https://www.pisos.com/venta/casas-benalmadena/con-3-habitaciones/hasta-300000/fecharecientedesde-desc/%s' % page for page in range(1,3)]
    base_url = 'https://www.pisos.com'

    def parse(self, response):
        all_homes = response.xpath('//div[@id="parrilla"]/div/@data-navigate-ref').extract()
  
        for home in all_homes:
            home_url = home
            home_url = self.base_url + home_url
            yield scrapy.Request(home_url, callback=self.parse_home)
        pass

    def parse_home(self, response):
        
        title = response.xpath('normalize-space(//div[@class="maindata-info"]/h1/text())').extract_first()

        price = response.xpath('normalize-space(//span[@class="h1 jsPrecioH1"]/text())').extract()
        price[0] = int(re.sub(r'[^0-9]', '', price[0])) # removed € symbol

        location = response.xpath('normalize-space(//div[@class="maindata-info"]/h2/text())').extract_first()

        description = response.xpath('normalize-space(//div[@id="descriptionBody"]/text())').extract()

        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        size = response.xpath('normalize-space(//div[@class="basicdata-item"][1])').extract()
        size[0] = re.sub(r'[^0-9]', '', size[0])

        pricem = int(int(price[0]) / int(size[0]))
        
        url = response.url

        yield {
            'title': title,         
            'price': price,
            'location': location,
            'description': description,
            'timestamp': timestamp,
            'pricem': pricem,
            'url': url
        }