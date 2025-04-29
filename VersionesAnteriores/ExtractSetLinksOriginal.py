import os
import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin, urlparse, urlunparse

def ExtractSetLinks(set_links):

    base_url = "https://onepiece.limitlesstcg.com"
    cards_url = f"{base_url}/cards"

    # Informacion inicial para pull de links
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(cards_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extraccion de los links
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/cards/") and "-" in href and href.count("/") == 2:
            full_url = base_url + href
            if full_url not in set_links:
                set_links.append(full_url)
                
    print(f"✅ Extracted {len(set_links)} set URLs")
    #print(set_links) 

    # Salvar a .txt 
    with open("set_links.txt", "w", encoding="utf-8") as file:
        for url in sorted(set_links):
            file.write(url + "\n")

