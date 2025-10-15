from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import pandas as pd

options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

items = []  
linksss = []

process = True
current_page = 1

#get contractor links
while process:
    print(f"processing page {current_page}")
    driver.get(f"https://muqawil.org/ar/contractors?page={current_page}")
    input("After doing the captcha press Enter :)")
    soup = BeautifulSoup(driver.page_source, "lxml")
    all_urls = soup.find_all("h1", class_="card-title")

    if current_page > 2:   # limit pages for testing
        print("page limit reached:::")
        process = False
        break

    for url in all_urls:
        link = url.find("a").get("href")
        linksss.append(link)
        print(link)

    current_page += 1

#open each url and scrape info
for link in linksss:
    print(f"processing link: {link}")
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, "lxml")

    labels = [lbl.get_text(strip=True) for lbl in soup.find_all("div", class_="info-name")]
    values = []

    for val in soup.find_all("div", class_="info-value"):
        link_val = val.find("a")
        if link_val:
            values.append(link_val.get_text(strip=True))
        else:
            values.append(val.get_text(strip=True))


    itemss = dict(zip(labels, values))


    title_tag = soup.find("h1", class_="inner-header__title")
    if title_tag:
        itemss["contractors names"] = title_tag.get_text(strip=True)


    itemss["links"] = link


    items.append(itemss)

#saves to excel
df = pd.DataFrame(items)
df.to_excel("contractors_info213.xlsx", index=False, engine="openpyxl")

print("Saved contractors_info2134.xlsx with headers + values")
driver.quit()
