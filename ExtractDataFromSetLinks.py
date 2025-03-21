import os
import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin, urlparse, urlunparse

# Path to your input file
file_path = r"C:\Users\INFESTED\Documents\GitHub\OPProject\set_links.txt"
base_dir = os.path.dirname(file_path)

# Folder to save the JSON files
cards_dir = os.path.join(base_dir, "Cards")
os.makedirs(cards_dir, exist_ok=True)

# Read the links from the file
with open(file_path, 'r') as file:
    links = file.read().splitlines()

# Loop through each link
for link in links:
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

        # Create a safe filename from the URL
        file_name = re.sub(r'\W+', '_', link.split('/')[-1]) or "index"
        json_file_path = os.path.join(cards_dir, f"{file_name}.json")

        # Save the data
        with open(json_file_path, 'w') as json_file:
            json.dump({'card_urls': card_urls, 'image_urls': image_urls}, json_file, indent=2)

        print(f"Saved: {json_file_path}")

    except Exception as e:
        print(f"Error processing {link}: {e}")
