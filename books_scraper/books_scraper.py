from bs4 import BeautifulSoup
import requests
import pandas as pd

current_page = 1
process = True
data = []

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

while process:
    print(f"scraping page {current_page}.....")

    url = "https://books.toscrape.com/catalogue/page-" + str(current_page) + ".html"
    page = requests.get(url)

    if page.status_code == 404:
        process = False
        break

    soup = BeautifulSoup(page.content, 'html.parser')

    all_books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

    for book in all_books:
        item = {}

        item['title'] = book.find("img").attrs["alt"]
        item['price'] = book.find("p", class_="price_color").text[2:]
        item['link'] = "https://books.toscrape.com/catalogue/" + book.find("a").attrs["href"]
        item['stock'] = book.find("p", class_="instock availability").text.strip()

        # Get star rating as text
        rating_tag = book.find("p", class_="star-rating")
        rating_classes = rating_tag.get("class") if rating_tag else []
        rating_text = rating_classes[1] if len(rating_classes) > 1 else "No rating"

        item['star_rating_text'] = rating_text
        item['star_rating'] = rating_map.get(rating_text, 0)  # numeric rating

        data.append(item)

    current_page += 1

df = pd.DataFrame(data)
df.to_csv("data1.csv", index=False)
print(f"Scraped {len(data)} books.")
