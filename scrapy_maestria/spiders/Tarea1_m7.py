from pathlib import Path

import scrapy

import scrapy
class EmpleoSpider(scrapy.Spider):
    name = "empleo"

    start_urls = ["https://trabajando.com.bo/trabajo"]

    def parse(self, response):
        empleo_page_links = response.css("h2.views-field-title a::attr(href)").getall()
        print('Inside parse')
        yield from response.follow_all(empleo_page_links, self.parse_empleo)

        next_links = response.css('a[title="Ir a la página siguiente"]')
        yield from response.follow_all(next_links, self.parse)

    def parse_empleo(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()
        yield {
            "name": extract_with_css("h1.trabajando-page-header > span::text"),
            "empresa": extract_with_css("div.views-field-field-nombre-empresa a::text"),
            "ubicacion": extract_with_css("div.views-field-field-ubicacion-del-empleo > div::text"),
            "tipo": extract_with_css("div.views-field-field-tipo-empleo > div::text"),
            "fecha_publicacion": extract_with_css("div.views-field-created time::text"),
            "fecha_vencimiento": extract_with_css("div.views-field-field-fecha-empleo-1 > div::text")

        }
    
    # def parse_author(self, response):
    #     def extract_with_css(query):
    #         return response.css(query).get(default="").strip()

    #     yield {
    #         "name": extract_with_css("h3.author-title::text"),
    #         "birthdate": extract_with_css(".author-born-date::text"),
    #         "bio": extract_with_css(".author-description::text"),
    #     }