# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Request


class ProfesescomSpider(Spider):
    name = 'profesEscom'
    allowed_domains = ['misprofesores.com']
    start_urls = ['http://www.misprofesores.com/escuelas/IPN-ESCOM_1694/']

    def parse(self, response):
        tabla = response.css(".profesores_table")[0]
        links = tabla.css("tbody a::attr(href)").extract()[1:]
        for link in links:
            yield Request(link, callback=self.parse_profe)

    def parse_profe(self, response):
        content = response.css("#content_profesor")[0]
        prof_name = content.css("div>h2>b>span::text").extract_first()
        c_trs = content.css(".calificaciones_table>tbody>tr")
        for c_tr in c_trs:
            comentario = {
                "profesor": prof_name,
                "fecha": c_tr.xpath("./td[1]/text()").extract_first(),
                "clase": c_tr.xpath("./td[2]/text()").extract_first(),
                "f": c_tr.xpath("./td[3]/b/text()").extract_first(),
                "a": c_tr.xpath("./td[4]/b/text()").extract_first(),
                "c": c_tr.xpath("./td[5]/b/text()").extract_first(),
                "comentario": c_tr.xpath("./td[8]/text()").extract_first()
            }
            yield comentario

        if not 'prof_name' in response.meta:
            pages = content.css("ul.pagination>li:not(.active)>a::attr(href)")
            pages = pages[:-1].extract()
            for page in pages:
                yield Request(page, callback=self.parse_profe, meta={"prof_name": prof_name})
        

