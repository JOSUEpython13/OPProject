import os
import json
import requests
from bs4 import BeautifulSoup

base_path = r"C:\Users\INFESTED\Documents\GitHub\OPProject\Cards"
headers = {"User-Agent": "Mozilla/5.0"}

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
                        print(f"Failed to load {url}")
                        continue

                    soup = BeautifulSoup(response.text, "html.parser")
                    card_text_div = soup.find("div", class_="card-text")

                    if card_text_div:
                        ccard_text = card_text_div.get_text(separator="\n", strip=True)
                        lines = ccard_text.splitlines()
                        
                        filtered_lines = []
                        skip_next = False
                        
                        for line in lines:
                            if skip_next:
                                skip_next = False
                                continue
                            if line.startswith("Illustrated by"):
                                skip_next = True
                                continue
                            filtered_lines.append(line)
                        
                        output_path = os.path.join(output_folder, f"{card_id}.txt")
                        with open(output_path, "w", encoding="utf-8") as out_file:
                            out_file.write("\n".join(filtered_lines))
                    else:
                        print(f"No card-text found in {url}")

                except Exception as e:
                    print(f"Error processing {url}: {e}")
