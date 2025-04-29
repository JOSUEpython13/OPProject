# ExtractCardInfo.py

import os
import json
import requests
from bs4 import BeautifulSoup

def extract_card_info(base_path=None):
    if base_path is None:
        base_path = os.path.join(os.getcwd(), "Cards")
    headers = {"User-Agent": "Mozilla/5.0"}

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

        effect_lines = []
        start_index = -1
        for idx, line in enumerate(lines):
            if line.startswith("["):
                start_index = idx
                break

        if start_index != -1:
            effect_lines = lines[start_index:-1] if lines[-1] not in categories and lines[-1] != result["card_code"] else lines[start_index:]
            result["effect"] = " ".join(effect_lines).strip()

        if lines and lines[-1] not in effect_lines:
            result["type"] = lines[-1]

        if result["category"] in {"Stage", "Event"}:
            result["counter"] = ""

        return "\n".join([f"{{{key}}}{value}" for key, value in result.items()])

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
                            print(f"❌ Failed to load {url}")
                            continue

                        soup = BeautifulSoup(response.text, "html.parser")
                        card_text_div = soup.find("div", class_="card-text")

                        allow_counter = True
                        meta_section = soup.find("p", class_="card-text-section")
                        if meta_section and "Counter" not in meta_section.get_text():
                            allow_counter = False

                        if card_text_div:
                            raw_text = card_text_div.get_text(separator="\n", strip=True)
                            lines = raw_text.splitlines()

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
                            print(f"❌ No card-text found in {url}")

                    except Exception as e:
                        print(f"❌ Error processing {url}: {e}")
                        
def extract_card_images(base_path=None):
    if base_path is None:
        base_path = os.path.join(os.getcwd(), "Cards")

    headers = {"User-Agent": "Mozilla/5.0"}

    if not os.path.exists(base_path):
        print(f"❌ Error: No se encontró la carpeta {base_path}")
        return

    for file_name in os.listdir(base_path):
        if file_name.endswith(".json"):
            json_path = os.path.join(base_path, file_name)
            folder_name = os.path.splitext(file_name)[0]

            set_folder = os.path.join(base_path, folder_name)
            images_folder = os.path.join(set_folder, "images")
            os.makedirs(images_folder, exist_ok=True)

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                card_urls = data.get("card_urls", [])
                image_urls = data.get("image_urls", [])

                if len(card_urls) != len(image_urls):
                    print(f"⚠️ Warning: {file_name} - Mismatch between cards and images count!")

                for idx, (card_url, image_url) in enumerate(zip(card_urls, image_urls)):
                    try:
                        if image_url.startswith("/"):
                            image_url = "https://limitlesstcg.nyc3.cdn.digitaloceanspaces.com" + image_url
                        
                        # Get card ID from URL to find matching txt
                        card_id = card_url.split("/cards/")[-1].split("?")[0]

                        # Determine extension from image URL
                        image_extension = image_url.split(".")[-1].split("?")[0]  # webp, jpg, etc.
                        image_filename = f"{card_id}.{image_extension}"

                        image_path = os.path.join(images_folder, image_filename)

                        response = requests.get(image_url, headers=headers)
                        if response.status_code == 200:
                            with open(image_path, "wb") as img_file:
                                img_file.write(response.content)
                            print(f"✅ Saved {image_filename}")
                        else:
                            print(f"❌ Failed to download {image_url}")

                    except Exception as e:
                        print(f"❌ Error downloading {image_url}: {e}")

    print("\n✅ Proceso de descarga de imágenes finalizado correctamente.")

def generate_card_htmls(base_path=None):
    if base_path is None:
        base_path = os.path.join(os.getcwd(), "Cards")

    if not os.path.exists(base_path):
        print(f"❌ Error: No se encontró la carpeta {base_path}")
        return

    for set_folder_name in os.listdir(base_path):
        set_folder = os.path.join(base_path, set_folder_name)
        if not os.path.isdir(set_folder):
            continue  # skip .json files etc

        images_folder = os.path.join(set_folder, "images")
        if not os.path.exists(images_folder):
            print(f"⚠️ No hay carpeta de imágenes en {set_folder_name}, saltando...")
            continue

        for file_name in os.listdir(set_folder):
            if file_name.endswith(".txt"):
                card_id = os.path.splitext(file_name)[0]
                txt_path = os.path.join(set_folder, file_name)
                image_extensions = ['.webp', '.jpg', '.png']

                # Search for image
                image_path = None
                for ext in image_extensions:
                    possible_image_path = os.path.join(images_folder, f"{card_id}{ext}")
                    if os.path.exists(possible_image_path):
                        image_path = os.path.relpath(possible_image_path, set_folder)
                        break

                if image_path is None:
                    print(f"❌ Imagen no encontrada para {card_id}, se omite.")
                    continue

                # Read the text info
                with open(txt_path, "r", encoding="utf-8") as txt_file:
                    card_info = txt_file.read()

                # Create the HTML file
                html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{card_id}</title>
</head>
<body>
<h1>{card_id}</h1>
<pre>
{card_info}
</pre>

<img src="{image_path}" alt="{card_id}" style="width:300px;"/>

</body>
</html>"""

                html_path = os.path.join(set_folder, f"{card_id}.html")
                with open(html_path, "w", encoding="utf-8") as html_file:
                    html_file.write(html_content)

                print(f"✅ HTML generado: {html_path}")

    print("\n✅ Todos los archivos HTML han sido generados correctamente.")
    
import os

def generate_index_html(base_path=None):
    if base_path is None:
        base_path = os.path.join(os.getcwd(), "Cards")

    if not os.path.exists(base_path):
        print(f"❌ La carpeta {base_path} no existe.")
        return

    html_sections = []

    for set_folder_name in sorted(os.listdir(base_path)):
        set_folder_path = os.path.join(base_path, set_folder_name)
        if not os.path.isdir(set_folder_path):
            continue

        card_links = []
        for file_name in sorted(os.listdir(set_folder_path)):
            if file_name.endswith(".html"):
                card_path = os.path.join(set_folder_name, file_name)
                card_links.append(f'<li><a href="{card_path}" target="_blank">{file_name}</a></li>')

        if card_links:
            section = f"""
<h2>{set_folder_name}</h2>
<ul>
{''.join(card_links)}
</ul>
"""
            html_sections.append(section)

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>One Piece TCG - Card Index</title>
</head>
<body>
<h1>One Piece TCG - Card HTML Index</h1>
{''.join(html_sections)}
</body>
</html>"""

    index_path = os.path.join(base_path, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)

    print(f"\n✅ Archivo index.html creado en {index_path}")
