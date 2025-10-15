
from bs4 import BeautifulSoup
import requests
import pandas as pd

current_page = 1

process = True

data= []

while(process == True):

     url = "https://www.amazon.ae/s?k=pixel+7+pro+screen+replacement&crid=365M65NFJAXJD&qid=1755050300&sprefix=pixel+7+pro+screen+%2Caps%2C181&xpid=jhfuyxSLzEeth&ref=sr_pg_"+str(current_page)+""

     page = requests.get(url)

     soup = BeautifulSoup(page.content, 'html.parser')

     products = soup.find_all('div', class_= 'a-section a-spacing-base')

     if not products:

         print("No products found")

         break

     else:

         for product in products:

              item = {}

              item['name'] = product.find('h2').text

              item['price'] = product.find('a').attrs =(product.find('span', class_= 'a-price-whole').text.strip(".") + 'AED')

              rating_tag = product.find("span", class_="a-icon-alt")

              item["rating"] = rating_tag.get_text(strip=True) if rating_tag else None


              data.append(item)





     current_page += 1

df = pd.DataFrame(data)
df.to_csv('product1s.csv')


