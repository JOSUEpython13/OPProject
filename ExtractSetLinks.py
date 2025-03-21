import requests
from bs4 import BeautifulSoup

base_url = "https://onepiece.limitlesstcg.com"
cards_url = f"{base_url}/cards"

# Fetch the main cards page
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(cards_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Extract set links
set_links = []
for link in soup.find_all("a", href=True):
    href = link["href"]
    if href.startswith("/cards/") and "-" in href and href.count("/") == 2:
        full_url = base_url + href
        if full_url not in set_links:
            set_links.append(full_url)

# Save to .txt file
with open("set_links.txt", "w", encoding="utf-8") as file:
    for url in sorted(set_links):
        file.write(url + "\n")

print(f"✅ Extracted {len(set_links)} set URLs to 'set_links.txt'")
