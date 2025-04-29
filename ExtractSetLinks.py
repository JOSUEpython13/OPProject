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

def save_set_links(set_links, path="set_links.json"):
    with open(path, "w") as f:
        json.dump(set_links, f, indent=2)

def load_set_links(path="set_links.json"):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def Extract_data_sets(set_links):   
    # Folder para salvar los JSON files
    base_dir = os.getcwd()
    cards_dir = os.path.join(base_dir, "Cards")
    os.makedirs(cards_dir, exist_ok=True)
    
    for link in set_links:
        try:
            response = requests.get(link)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            card_urls = []
            image_urls = []

            for a_tag in soup.select('div.card-search-grid a[href]'):
                raw_url = urljoin(link, a_tag['href'])
                parsed_url = urlparse(raw_url)
                clean_url = urlunparse(parsed_url._replace(query=''))  # removes '?v=...'
                card_urls.append(clean_url)

                img_tag = a_tag.find('img')
                if img_tag and img_tag.get('src'):
                    image_url = img_tag['src']
                    image_urls.append(image_url)

            # Creacion de nombre del archivo
            file_name = re.sub(r'\W+', '_', link.split('/')[-1]) or "index"
            json_file_path = os.path.join(cards_dir, f"{file_name}.json")

            # Save de la informacion
            with open(json_file_path, 'w') as json_file:
                json.dump({'card_urls': card_urls, 'image_urls': image_urls}, json_file, indent=2)

            print(f"Saved: {json_file_path}")

        except Exception as e:
            print(f"Error processing {link}: {e}")