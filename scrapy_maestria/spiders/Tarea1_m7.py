from pathlib import Path

import scrapy

from datetime import datetime  # Importa la librería datetime
class EmpleoSpider(scrapy.Spider):
    name = "empleo"

    start_urls = ["https://trabajando.com.bo/trabajo","https://trabajito.com.bo/trabajo"]

    def parse(self, response):
        url_site = response.url
        if 'trabajando' in url_site:
            empleo_page_links = response.css("h2.views-field-title a::attr(href)").getall()
            print('Inside parse')
            yield from response.follow_all(empleo_page_links, self.parse_trabajando)

            # next_links = response.css('a[title="Ir a la página siguiente"]')
            # yield from response.follow_all(next_links, self.parse)
        elif 'trabajito' in url_site:
            empleo_page_links = response.css("div.job-block h4 a::attr(href)").getall()
            print('Inside trabajito')
            yield from response.follow_all(empleo_page_links, self.parse_trabajito)

            # next_links = response.css('a[rel="next"]')
            # yield from response.follow_all(next_links, self.parse)
    

    def parse_trabajando(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()
        yield {
            "url": response.url,
            "name": extract_with_css("h1.trabajando-page-header > span::text"),
            "empresa": extract_with_css("div.views-field-field-nombre-empresa a::text"),
            "ubicacion": extract_with_css("div.views-field-field-ubicacion-del-empleo > div::text"),
            "tipo": extract_with_css("div.views-field-field-tipo-empleo > div::text"),
            "fecha_publicacion": extract_with_css("div.views-field-created time::text"),
            "fecha_vencimiento": extract_with_css("div.views-field-field-fecha-empleo-1 > div::text"),
            #"job_descripcion": wraper.css('div.field--type-text-with-summary div.field--item p::text').getall(),
            "fecha_guardar": datetime.now().isoformat()
             
        }
    
    def parse_trabajito(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()
        

        # Extrae el wrapper
        wrapper = response.css('section.job-detail')    
        job_desc = wrapper.css('ul.job-info li')
        job_overview = wrapper.css('aside.sidebar ul.job-overview li')

        yield {
            "url": response.url,
            "name": extract_with_css("h1.JobViewTitle::text"),
            "empresa": extract_with_css("h2::text"),
            "ubicacion": response.xpath("//li[h5[contains(text(),'Ubicación:')]]/span/text()" ).get(),
            "tipo": job_desc[0].css("::text").get() if job_desc else "No especificado",
            "fecha_publicacion": job_desc[2].css("li ::text").get() if job_desc else "No especificado",
            "fecha_vencimiento": job_overview[1].css("li span::text").get() if job_overview else "No especificado",
           # "job_descripcion": wrapper.css('div.job-detail.only-text p::text').getall(),
            "fecha_guardar": datetime.now().isoformat()

        }
    
    # def parse_author(self, response):
    #     def extract_with_css(query):
    #         return response.css(query).get(default="").strip()

    #     yield {
    #         "name": extract_with_css("h3.author-title::text"),
    #         "birthdate": extract_with_css(".author-born-date::text"),
    #         "bio": extract_with_css(".author-description::text"),
    #     }