import os
import json
import requests
from bs4 import BeautifulSoup

base_path = r"C:\Users\INFESTED\Documents\GitHub\OPProject\Cards"
headers = {"User-Agent": "Mozilla/5.0"}

# --- Card Parsing Logic ---
def parse_card_text(card_lines):
    result = {
        "card_name": "",
        "card_code": "",
        "category": "",
        "color": "",
        "cost": "",
        "power": "",
        "atributte": "",
        "counter": "",
        "effect": "",
        "type": ""
    }

    categories = {"Character", "Leader", "Event", "Stage"}
    colors = {"Black", "Yellow", "Red", "Blue", "Green", "Purple"}
    attributes = {"Slash", "Strike", "Ranged", "Special", "Wisdom"}

    lines = [line.strip() for line in card_lines if line.strip()]

    if lines:
        result["card_name"] = lines[0]
    if len(lines) > 1:
        result["card_code"] = lines[1]

    for line in lines:
        if line in categories:
            result["category"] = line
            break

    for line in lines:
        if any(color in line for color in colors):
            result["color"] = " / ".join([color for color in colors if color in line])
            break

    for line in lines:
        if "Cost" in line:
            result["cost"] = line.replace("•", "").replace("Cost", "").strip()
            break

    for line in lines:
        if "Power" in line:
            result["power"] = line.replace("Power", "").strip()
            break

    for line in lines:
        if any(attr in line for attr in attributes):
            result["atributte"] = " / ".join([attr for attr in attributes if attr in line])
            break

    for line in lines:
        if "+1000" in line or "+2000" in line:
            result["counter"] = line.replace("+", "").strip()
            break
        elif "Counter" in line:
            result["counter"] = line.replace("Counter", "").strip()
            break

    for line in lines:
        if line.startswith("["):
            result["effect"] = line
            break

    result["type"] = lines[-1] if lines else ""

    return "\n".join([f"{{{key}}}{value}" for key, value in result.items()])


# --- Main Script ---
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
                        raw_text = card_text_div.get_text(separator="\n", strip=True)
                        lines = raw_text.splitlines()

                        # Remove "Illustrated by" and next line
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

                        formatted_card = parse_card_text(filtered_lines)

                        output_path = os.path.join(output_folder, f"{card_id}.txt")
                        with open(output_path, "w", encoding="utf-8") as out_file:
                            out_file.write(formatted_card)
                    else:
                        print(f"No card-text found in {url}")

                except Exception as e:
                    print(f"Error processing {url}: {e}")
