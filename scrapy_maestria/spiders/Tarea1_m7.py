from pathlib import Path

import scrapy
import uuid

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

            next_links = response.css('a[title="Ir a la página siguiente"]')
            yield from response.follow_all(next_links, self.parse)
        elif 'trabajito' in url_site:
             # Extraer información antes de seguir el enlace
            for job in response.css("div.job-block"):
                job_link = job.css("h4 a::attr(href)").get()
                
                tipo = job.css("li.time::text").get(default="No especificado").strip()
            
                if job_link:
                    yield response.follow(
                        job_link,
                        self.parse_trabajito,
                        meta={
                            "tipo": tipo,
                        }
                    )


            next_links = response.css('a[rel="next"]')
            yield from response.follow_all(next_links, self.parse)
    

    def parse_trabajando(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()
        yield {
            "data_id": str(uuid.uuid4()),
            "url": response.url,
            "name": extract_with_css("h1.trabajando-page-header > span::text"),
            "empresa": extract_with_css("div.views-field-field-nombre-empresa a::text"),
            "ubicacion": extract_with_css("div.views-field-field-ubicacion-del-empleo > div::text"),
            "tipo": extract_with_css("div.views-field-field-tipo-empleo > div::text"),
            "requisitos": response.xpath("//li[h5[contains(text(),'Requisitos:')]]/span/text()").get(default="No especificado"),    
            "fecha_publicacion": extract_with_css("div.views-field-created time::text"),
            "fecha_vencimiento": extract_with_css("div.views-field-field-fecha-empleo-1 > div::text"),
            "job_descripcion": response.css('div.field--type-text-with-summary div.field--item p::text').getall(),
            "fecha_guardar": datetime.now().isoformat()
             
        }
    
    def parse_trabajito(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()

        # Obtener los datos que pasamos con meta en parse()
        tipo = response.meta.get("tipo", "No especificado")

        yield {
            "data_id": str(uuid.uuid4()),
            "url": response.url,
            "name": extract_with_css("h1.JobViewTitle::text"),
            "empresa": extract_with_css("h2::text"),
            "ubicacion": response.xpath("//li[h5[contains(text(),'Ubicación:')]]/span/text()").get(default="No especificado"),
            "tipo": tipo,
            "fecha_publicacion": response.xpath("//li[h5[contains(text(),'Fecha de publicación:')]]/span/text()").get(default="No especificado"),
            "fecha_vencimiento": response.xpath("//li[h5[contains(text(),'Fecha de caducidad:')]]/span/text()").get(default="No especificado"),
            "job_descripcion": response.css('div.job-detail.only-text p::text').getall(), 
            "fecha_guardar": datetime.now().isoformat()
        }