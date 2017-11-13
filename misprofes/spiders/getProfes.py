# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Request


class GetprofesSpider(Spider):
    name = 'getProfes'
    allowed_domains = ['www.misprofesores.com']
    start_urls = ['http://www.misprofesores.com/escuelas/IPN-ESCOM_1694/']

    def parse(self, response):
        tabla = response.css(".profesores_table")[0]
        links = tabla.css("tbody a::attr(href)").extract()[1:]
        for link in links:
            yield Request(link, callback=self.parse_profe)

    def parse_profe(self, response):
        content = response.css("#content_profesor")[0]
        name = content.css("div>h2>b>span::text").extract_first()
        prom_general = content.css(
            "span.rating span.average::text").extract_first()
        prom_facilidad = content.xpath("./div[1]/b[1]/text()").extract_first()
        prom_ayuda = content.xpath("./div[1]/b[2]/text()").extract_first()
        prom_claridad = content.xpath("./div[1]/b[3]/text()").extract_first()
        data_prof = {
            "name": name,
            "prom_general": prom_general,
            "prom_facilidad": prom_facilidad,
            "prom_ayuda": prom_ayuda,
            "prom_claridad": prom_claridad
        }
        yield data_prof
