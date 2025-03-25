import scrapy
from pathlib import Path
import datetime
import csv


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    def start_requests(self):
        urls = [
            "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        bookdetail = []
        # Path(filename).write_bytes(response.body)

        self.log(f"Saved file {filename}")
        cards = response.css(".product_pod")
        for card in cards:
            title = card.css("h3>a::text").get()

            rating = card.css(".star-rating").attrib["class"].split(" ")[1]

            # price = card.css(".product_price>p::text").get()
            price = card.css(".price_color::text").get()

            availablity = card.css(".availability")
            if len(availablity.css(".icon-ok")) > 0:
                   inStock = True
            else:
                   inStock = False

            # image = card.css(".image_container img").get()
            image = card.css(".image_container img")
            image = image.attrib["src"] 
            bookdetail.append({
                "title": title,
                "rating": rating,
                "price": price,
                "in_stock": inStock,
                "image_url": image,
            })
            # Save to CSV
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bookdetail_{timestamp}.csv"
            
            keys = bookdetail[0].keys() if bookdetail else []
            
            with open(filename, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(bookdetail)
            
            self.log(f"Saved data to {filename}")
        