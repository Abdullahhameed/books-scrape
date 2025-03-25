import scrapy
from pathlib import Path
from pymongo import MongoClient
import datetime


client = MongoClient("mongodb+srv://abdullahhameed66:udLWW5DeymtTeVws@bookscrapy.s2rd1.mongodb.net/?retryWrites=true&w=majority&appName=BookScrapy")
db = client.scrapy

def insertToDB(page, title, rating, image, price, inStock):
     collections = db[page]

     doc = {
        "title": title,
        "rating": rating,
        "image": image,
        "price": price,
        "inStock": inStock,
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }
     
     inserted = collections.insert_one(doc)
     return inserted.inserted_id

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
        bookdetail = {}
        # Path(filename).write_bytes(response.body)

        self.log(f"Saved file {filename}")
        cards = response.css(".product_pod")
        for card in cards:
            title = card.css("h3>a::text").get()
            print(title)

            rating = card.css(".star-rating").attrib["class"].split(" ")[1]
            print(rating)

            # price = card.css(".product_price>p::text").get()
            price = card.css(".price_color::text").get()
            print(price)

            availablity = card.css(".availability")
            if len(availablity.css(".icon-ok")) > 0:
                   inStock = True
            else:
                   inStock = False
            print(inStock)

            # image = card.css(".image_container img").get()
            image = card.css(".image_container img")
            image = image.attrib["src"] 
            print(image)
            insertToDB(page, title, rating, image, price, inStock)
        