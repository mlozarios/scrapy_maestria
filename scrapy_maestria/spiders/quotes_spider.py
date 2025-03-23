import scrapy

class JobSpider(scrapy.Spider):
    name = "jobs"

    # Agregamos las URLs de ambas páginas
    start_urls = [
        "https://www.trabajando.com.bo/",
        "https://www.trabajopolis.bo/"
    ]

    def parse(self, response):
        # Identificar de qué página viene la respuesta
        if "trabajando.com.bo" in response.url:
            job_links = response.css(".job-title a::attr(href)").getall()
            next_page = response.css(".next-page a::attr(href)").get()
        elif "trabajopolis.bo" in response.url:
            job_links = response.css(".job-listing a::attr(href)").getall()
            next_page = response.css(".pagination-next a::attr(href)").get()

        # Seguir los enlaces de cada oferta de trabajo
        for link in job_links:
            yield response.follow(link, callback=self.parse_job)

        # Seguir a la siguiente página si existe
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_job(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()

        # Extraer información de cada oferta de trabajo
        yield {
            "title": extract_with_css("h1::text"),
            "company": extract_with_css(".company-name::text"),
            "location": extract_with_css(".location::text"),
            "description": extract_with_css(".job-description::text"),
            "url": response.url
        }
