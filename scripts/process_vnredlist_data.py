import requests
from bs4 import BeautifulSoup
import time

BASE = "http://vnredlist.vast.vn/dong-vat/dong-vat-co-day-song/lop-thu/"

######## HELPERS ########
# Function to get BeautifulSoup object from URL
def get_soup(url):
    r = requests.get(url)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

# Function to get species links from a page
def get_species_links(page):
    url = BASE if page == 1 else f"{BASE}page/{page}/"
    soup = get_soup(url)
    return [a["href"] for a in soup.select("div.cards article h2 a")]

# Function to scrape species detail from its page
def scrape_species_detail(url):
    soup = get_soup(url)

    articles = soup.select("article")
    if not articles:
        return ""

    blocks = []
    for art in articles:
        text = art.get_text("\n", strip=True)
        if text:
            blocks.append(text)

    return "\n\n".join(blocks)

######## MAIN ########
# Manually set max_page based on observation
max_page = 8

all_links = []

# Extract species links from all pages
for p in range(1, max_page + 1):
    print(f"Process page: {p}/{max_page}")
    links = get_species_links(p)
    all_links.extend(links)
    time.sleep(0.5)

# Unique
all_links = list(dict.fromkeys(all_links))
print("\nTotal species:", len(all_links))

results = {}
print("\nStart extracting detail of each species\n")
for idx, url in enumerate(all_links, 1):
    print(f"[{idx}/{len(all_links)}] {url}")
    try:
        content = scrape_species_detail(url)
        results[url] = content
    except Exception as e:
        print("Error: ", e)

    time.sleep(0.5)

# Save results
with open("dataset/processed_data.txt", "w", encoding="utf-8") as f:
    for url, text in results.items():
        f.write(f"{text}\n\n")

print("\nDONE! File saved")
