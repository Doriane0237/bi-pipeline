import requests
from bs4 import BeautifulSoup
from datetime import datetime
from supabase import create_client
import os

# Get credentials from GitHub Secrets
url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]

supabase = create_client(url, key)

def scrape_category(url, category_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.find_all("div", class_="thumbnail")

    data = []
    scraped_at = datetime.now().isoformat()

    for product in products:
        name = product.find("a", class_="title").text.strip()
        price = product.find("h4", class_="price").text.strip().replace("$", "")

        rating_tag = product.find("p", attrs={"data-rating": True})
        rating = int(rating_tag["data-rating"]) if rating_tag else 0

        data.append({
            "name": name,
            "price": float(price),
            "rating": rating,
            "category": category_name,
            "scraped_at": scraped_at
        })

    return data


all_data = []
all_data += scrape_category("https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops", "laptops")
all_data += scrape_category("https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets", "tablets")
all_data += scrape_category("https://webscraper.io/test-sites/e-commerce/allinone/phones/touch", "phones")

# Insert into Supabase
supabase.table("products").insert(all_data).execute()
