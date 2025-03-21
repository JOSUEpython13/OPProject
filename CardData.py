import os
import json
import requests
from bs4 import BeautifulSoup

# Base path to the folder containing JSON files
base_path = r"C:\Users\INFESTED\Documents\GitHub\OPProject\Cards"

# Headers to mimic a real browser request
headers = {"User-Agent": "Mozilla/5.0"}

def safe_get_text(element, default="N/A"):
    """Safely extract text from a BeautifulSoup element."""
    return element.text.strip() if element else default

def safe_get_attr(element, attr, default="N/A"):
    """Safely extract an attribute from a BeautifulSoup element."""
    return element[attr] if element and element.has_attr(attr) else default

# Iterate over all JSON files in the base path
for file_name in os.listdir(base_path):
    if file_name.endswith(".json"):
        json_path = os.path.join(base_path, file_name)
        folder_name = os.path.splitext(file_name)[0]
        output_folder = os.path.join(base_path, folder_name)
        os.makedirs(output_folder, exist_ok=True)

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            card_urls = data.get("card_urls", [])

            for url in card_urls:
                try:
                    card_id = url.split("/cards/")[-1].split("?")[0]
                    response = requests.get(url, headers=headers)
                    if response.status_code != 200:
                        print(f"Failed to retrieve {url}: Status code {response.status_code}")
                        continue

                    soup = BeautifulSoup(response.text, "html.parser")

                    # Extract card details with safety checks
                    card_name = safe_get_text(soup.find("span", class_="card-text-name"))
                    full_card_id = safe_get_text(soup.find("span", class_="card-text-id"))
                    card_type = safe_get_text(soup.find("p", class_="card-text-type"))
                    card_power = safe_get_text(soup.find("p", class_="card-text-section"))

                    abilities = soup.find_all("div", class_="card-text-section")
                    card_abilities = [a.text.strip() for a in abilities if "{SWORD}" in a.text or "{Navy}" in a.text]

                    illustrator_tag = soup.find("div", class_="card-text-artist")
                    illustrator = safe_get_text(illustrator_tag.find("a") if illustrator_tag else None)

                    image_url = safe_get_attr(soup.find("img", class_="card"), "src")

                    # Write card details to a text file
                    output_path = os.path.join(output_folder, f"{card_id}.txt")
                    with open(output_path, "w", encoding="utf-8") as out_file:
                        out_file.write(f"Card Name: {card_name}\n")
                        out_file.write(f"Card ID: {full_card_id}\n")
                        out_file.write(f"Card Type: {card_type}\n")
                        out_file.write(f"Card Power: {card_power}\n")
                        out_file.write(f"Abilities: {' '.join(card_abilities)}\n")
                        out_file.write(f"Illustrator: {illustrator}\n")
                        out_file.write(f"Image URL: {image_url}\n")

                except Exception as e:
                    print(f"Error processing {url}: {e}")
