import os
import json
import requests
from bs4 import BeautifulSoup

base_path = r"C:\Users\jsolanor\Documents\GitHub\OPProject\Cards"
headers = {"User-Agent": "Mozilla/5.0"}

#Funcion para leer cartas
def parse_card_text(card_lines, allow_counter=True):
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

    if allow_counter:
        for line in lines:
            if "+1000" in line or "+2000" in line:
                result["counter"] = line.replace("+", "").strip()
                break
            elif "Counter" in line and not line.startswith("[Counter]"):
                result["counter"] = line.replace("Counter", "").strip()
                break
    else:
        result["counter"] = ""

    # Robust multi-line effect block (capture from first "[" until end or known break)
    effect_lines = []
    start_index = -1
    for idx, line in enumerate(lines):
        if line.startswith("["):
            start_index = idx
            break

    if start_index != -1:
        effect_lines = lines[start_index:-1] if lines[-1] not in categories and lines[-1] != result["card_code"] else lines[start_index:]
        result["effect"] = " ".join(effect_lines).strip()

    # Final line is most likely type (but avoid duplication if it was in effect)
    if lines and lines[-1] not in effect_lines:
        result["type"] = lines[-1]

    # Force counter blank for Stage and Event
    if result["category"] in {"Stage", "Event"}:
        result["counter"] = ""

    return "\n".join([f"{{{key}}}{value}" for key, value in result.items()])


#MAIN - Core del Script
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

                    # Verificar el counter antes de la seccion de "power"
                    allow_counter = True
                    meta_section = soup.find("p", class_="card-text-section")
                    if meta_section and "Counter" not in meta_section.get_text():
                        allow_counter = False

                    if card_text_div:
                        raw_text = card_text_div.get_text(separator="\n", strip=True)
                        lines = raw_text.splitlines()

                        # Remover "Illustrated by" y la linea siguiente
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

                        formatted_card = parse_card_text(filtered_lines, allow_counter=allow_counter)

                        output_path = os.path.join(output_folder, f"{card_id}.txt")
                        with open(output_path, "w", encoding="utf-8") as out_file:
                            out_file.write(formatted_card)
                    else:
                        print(f"No card-text found in {url}")

                except Exception as e:
                    print(f"Error processing {url}: {e}")
