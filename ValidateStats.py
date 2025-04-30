import matplotlib.pyplot as plt
from collections import Counter
import os
import re

def normalize(text):
    return text.replace('–', '-').replace('—', '-').replace('‐', '-').replace(' ', '').strip().upper()

def validate_deck(base_path=None):
    if base_path is None:
        base_path = os.path.join(os.getcwd(), "Cards")

    deck_base = os.path.join(os.getcwd(), "Decks")

    if not os.path.exists(deck_base):
        print(f"❌ No se encontró la carpeta de Decks en {deck_base}")
        return

    available_decks = [f for f in os.listdir(deck_base) if f.endswith('.txt')]

    if not available_decks:
        print("❌ No hay archivos de deck disponibles en la carpeta Decks.")
        return

    print("\n=== Decks disponibles ===")
    for idx, deck_name in enumerate(available_decks, start=1):
        print(f"{idx}. {deck_name}")

    try:
        selected = int(input("\nSeleccione el número del deck que desea validar: "))
        if selected < 1 or selected > len(available_decks):
            print("❌ Selección inválida.")
            return
    except ValueError:
        print("❌ Entrada inválida.")
        return

    deck_file_path = os.path.join(deck_base, available_decks[selected - 1])
    print(f"\n🔍 Validando deck: {available_decks[selected - 1]}...\n")

    deck = []
    with open(deck_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                # Correct split using regex to handle missing spaces around 'x'
                parts = re.split(r'\s*x\s*', line.lower())
                if len(parts) == 2:
                    count, card_id = parts
                    card_id = normalize(card_id)
                    deck.append((int(count), card_id))

    leader_count = 0
    main_deck_count = 0
    errors = []

    all_card_txt_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith('.txt'):
                all_card_txt_files.append(os.path.join(root, file))

    print(f"🔎 Buscando {len(deck)} cartas en {len(all_card_txt_files)} archivos disponibles.\n")

    for count, card_id in deck:
        found = False
        card_type = None

        print(f"🔍 Buscando carta: {card_id} ...")

        for card_path in all_card_txt_files:
            file_card_id = normalize(os.path.splitext(os.path.basename(card_path))[0])
            if file_card_id == card_id:
                print(f"✅ Encontrado: {card_path}")
                with open(card_path, "r", encoding="utf-8") as card_file:
                    for line in card_file:
                        if line.startswith("{category}"):
                            category = line.replace("{category}", "").strip().lower()
                            if category == "leader":
                                card_type = "Leader"
                            else:
                                card_type = "MainDeck"
                            break
                found = True
                break

        if not found:
            print(f"❌ Carta no encontrada: {card_id}")
            errors.append(f"❌ Carta no encontrada: {card_id}")
            continue

        if card_type == "Leader":
            leader_count += count
        else:
            main_deck_count += count

        if count > 4:
            errors.append(f"❌ Más de 4 copias de la carta: {card_id} ({count} copias)")

    if leader_count != 1:
        errors.append(f"❌ Debe haber exactamente 1 carta Leader. Hay {leader_count}.")
    if main_deck_count != 50:
        errors.append(f"❌ Debe haber exactamente 50 cartas en el Main Deck. Hay {main_deck_count}.")

    print("\n=== Resultado de la validación ===")
    if errors:
        for e in errors:
            print(e)
        print("\n❌ Deck inválido.")
    else:
        print("✅ Deck válido.")
    print("===============================\n")

import os
import re

def normalize(text):
    return text.replace('–', '-').replace('—', '-').replace('‐', '-').replace(' ', '').strip().upper()

import os
import re

def normalize(text):
    return text.replace('–', '-').replace('—', '-').replace('‐', '-').replace(' ', '').strip().upper()

import os
import re

def normalize(text):
    return text.replace('–', '-').replace('—', '-').replace('‐', '-').replace(' ', '').strip().upper()

def export_deck_to_html_with_images(base_cards_path=None):
    if base_cards_path is None:
        base_cards_path = os.path.join(os.getcwd(), "Cards")

    deck_base = os.path.join(os.getcwd(), "Decks")
    output_html_base = os.path.join(os.getcwd(), "DeckExports")

    os.makedirs(output_html_base, exist_ok=True)

    available_decks = [f for f in os.listdir(deck_base) if f.endswith('.txt')]

    if not available_decks:
        print("❌ No hay archivos de deck disponibles.")
        return

    print("\n=== Decks disponibles para exportar ===")
    for idx, deck_name in enumerate(available_decks, start=1):
        print(f"{idx}. {deck_name}")

    try:
        selected = int(input("\nSeleccione el número del deck que desea exportar: "))
        if selected < 1 or selected > len(available_decks):
            print("❌ Selección inválida.")
            return
    except ValueError:
        print("❌ Entrada inválida.")
        return

    deck_file_path = os.path.join(deck_base, available_decks[selected - 1])
    deck_name = os.path.splitext(available_decks[selected - 1])[0]

    # Parse the deck
    deck = []
    with open(deck_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = re.split(r'\s*x\s*', line.lower())
                if len(parts) == 2:
                    count, card_id = parts
                    card_id = normalize(card_id)
                    deck.append((int(count), card_id))

    # Gather all card files
    all_card_txt_files = []
    for root, dirs, files in os.walk(base_cards_path):
        for file in files:
            if file.lower().endswith('.txt'):
                all_card_txt_files.append(os.path.join(root, file))

    deck_cards = []
    for count, card_id in deck:
        found = False
        card_name = "Unknown"
        card_folder = None
        for card_path in all_card_txt_files:
            file_card_id = normalize(os.path.splitext(os.path.basename(card_path))[0])
            if file_card_id == card_id:
                with open(card_path, "r", encoding="utf-8") as card_file:
                    card_text = card_file.read()
                    for line in card_text.splitlines():
                        if line.startswith("{card_name}"):
                            card_name = line.replace("{card_name}", "").strip()
                card_folder = os.path.basename(os.path.dirname(card_path))
                found = True
                break
        deck_cards.append((count, card_id, card_name, card_folder))

    # Separate Leader and Main Deck manually
    leader_card = None
    main_deck_cards = []

    for count, card_id, card_name, card_folder in deck_cards:
        if "leader" in card_name.lower() or card_id.startswith("OP08-098"):  # Fine tune for Kalgara deck
            leader_card = (count, card_id, card_name, card_folder)
        else:
            main_deck_cards.append((count, card_id, card_name, card_folder))

    # Sort Main Deck alphabetically
    main_deck_cards = sorted(main_deck_cards, key=lambda x: x[2])

    # Now generate HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Deck Export - {deck_name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f0f0f0;
        }}
        h1, h2 {{
            color: #333;
        }}
        .deck-container {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 10px;
            justify-items: center;
        }}
        .card {{
            width: 120px;
            text-align: center;
            background: white;
            padding: 8px;
            border-radius: 6px;
            box-shadow: 0 0 4px rgba(0,0,0,0.2);
        }}
        .card img {{
            width: 100%;
            height: auto;
            border-radius: 5px;
        }}
        .quantity {{
            font-weight: bold;
            color: darkgreen;
            font-size: 0.9em;
            margin-top: 4px;
        }}
        .leader {{
            border: 2px solid darkred;
        }}
    </style>
</head>
<body>
    <h1>Deck: {deck_name}</h1>
"""

    # Display Leader first
    if leader_card:
        count, card_id, card_name, card_folder = leader_card
        image_path = f"../Cards/{card_folder}/images/{card_id}.webp"
        html_content += "<h2>Leader</h2>\n<div class='deck-container'>\n"
        html_content += f"""<div class='card leader'>
            <img src="{image_path}" alt="{card_name}">
            <div class='quantity'>{count}x</div>
            <div>{card_name}</div>
            <div>({card_id})</div>
        </div>\n</div>\n"""

    # Main Deck
    html_content += "<h2>Main Deck</h2>\n<div class='deck-container'>\n"
    for count, card_id, card_name, card_folder in main_deck_cards:
        image_path = f"../Cards/{card_folder}/images/{card_id}.webp"
        html_content += f"""<div class='card'>
            <img src="{image_path}" alt="{card_name}">
            <div class='quantity'>{count}x</div>
            <div>{card_name}</div>
            <div>({card_id})</div>
        </div>\n"""
    html_content += "</div>\n"

    html_content += """
</body>
</html>
"""

    # Save the HTML
    output_file = os.path.join(output_html_base, f"{deck_name}.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n✅ Deck exportado exitosamente a: {output_file}")

def plot_deck_cost_curve(base_cards_path=None):
    if base_cards_path is None:
        base_cards_path = os.path.join(os.getcwd(), "Cards")

    deck_base = os.path.join(os.getcwd(), "Decks")
    available_decks = [f for f in os.listdir(deck_base) if f.endswith('.txt')]

    if not available_decks:
        print("❌ No hay archivos de deck disponibles.")
        return

    print("\n=== Decks disponibles para graficar ===")
    for idx, deck_name in enumerate(available_decks, start=1):
        print(f"{idx}. {deck_name}")

    try:
        selected = int(input("\nSeleccione el número del deck: "))
        if selected < 1 or selected > len(available_decks):
            print("❌ Selección inválida.")
            return
    except ValueError:
        print("❌ Entrada inválida.")
        return

    deck_file_path = os.path.join(deck_base, available_decks[selected - 1])

    # Leer deck
    deck = []
    with open(deck_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = re.split(r'\s*x\s*', line.lower())
                if len(parts) == 2:
                    count, card_id = parts
                    deck.append((int(count), normalize(card_id)))

    # Buscar archivos de carta
    all_card_txt_files = []
    for root, dirs, files in os.walk(base_cards_path):
        for file in files:
            if file.lower().endswith('.txt'):
                all_card_txt_files.append(os.path.join(root, file))

    # Contar costes
    cost_counter = Counter()

    for count, card_id in deck:
        for card_path in all_card_txt_files:
            file_card_id = normalize(os.path.splitext(os.path.basename(card_path))[0])
            if file_card_id == card_id:
                with open(card_path, "r", encoding="utf-8") as card_file:
                    for line in card_file:
                        if line.startswith("{cost}"):
                            try:
                                cost = int(line.replace("{cost}", "").strip())
                                cost_counter[cost] += count
                            except ValueError:
                                pass
                break

    # Crear gráfica
    if not cost_counter:
        print("❌ No se encontraron datos de coste.")
        return

    sorted_costs = sorted(cost_counter.items())
    x, y = zip(*sorted_costs)

    plt.bar(x, y, color='skyblue')
    plt.xlabel("Costo de carta")
    plt.ylabel("Cantidad de cartas")
    plt.title("Curva de Coste del Deck")
    plt.xticks(range(min(x), max(x)+1))
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()
    
def plot_deck_color_distribution(base_cards_path=None):
    if base_cards_path is None:
        base_cards_path = os.path.join(os.getcwd(), "Cards")

    deck_base = os.path.join(os.getcwd(), "Decks")
    available_decks = [f for f in os.listdir(deck_base) if f.endswith('.txt')]

    if not available_decks:
        print("❌ No hay decks disponibles.")
        return

    print("\n=== Decks disponibles ===")
    for idx, deck_name in enumerate(available_decks, start=1):
        print(f"{idx}. {deck_name}")
    try:
        selected = int(input("\nSeleccione el número del deck: "))
        if selected < 1 or selected > len(available_decks):
            print("❌ Selección inválida.")
            return
    except ValueError:
        print("❌ Entrada inválida.")
        return

    deck_file = os.path.join(deck_base, available_decks[selected - 1])
    deck = []
    with open(deck_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = re.split(r'\s*x\s*', line.lower())
                if len(parts) == 2:
                    count, card_id = parts
                    deck.append((int(count), normalize(card_id)))

    all_card_txt_files = []
    for root, dirs, files in os.walk(base_cards_path):
        for file in files:
            if file.endswith(".txt"):
                all_card_txt_files.append(os.path.join(root, file))

    from collections import Counter
    color_counter = Counter()

    for count, card_id in deck:
        for path in all_card_txt_files:
            if normalize(os.path.splitext(os.path.basename(path))[0]) == card_id:
                with open(path, "r", encoding="utf-8") as card_file:
                    for line in card_file:
                        if line.startswith("{color}"):
                            color = line.replace("{color}", "").strip()
                            color_counter[color] += count
                break

    if not color_counter:
        print("❌ No se encontraron colores.")
        return

    labels = list(color_counter.keys())
    sizes = list(color_counter.values())

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title("Distribución por Color del Deck")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()

def plot_deck_type_distribution(base_cards_path=None):
    if base_cards_path is None:
        base_cards_path = os.path.join(os.getcwd(), "Cards")

    deck_base = os.path.join(os.getcwd(), "Decks")
    available_decks = [f for f in os.listdir(deck_base) if f.endswith('.txt')]

    if not available_decks:
        print("❌ No hay decks disponibles.")
        return

    print("\n=== Decks disponibles ===")
    for idx, deck_name in enumerate(available_decks, start=1):
        print(f"{idx}. {deck_name}")
    try:
        selected = int(input("\nSeleccione el número del deck: "))
        if selected < 1 or selected > len(available_decks):
            print("❌ Selección inválida.")
            return
    except ValueError:
        print("❌ Entrada inválida.")
        return

    deck_file = os.path.join(deck_base, available_decks[selected - 1])
    deck = []
    with open(deck_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = re.split(r'\s*x\s*', line.lower())
                if len(parts) == 2:
                    count, card_id = parts
                    deck.append((int(count), normalize(card_id)))

    all_card_txt_files = []
    for root, dirs, files in os.walk(base_cards_path):
        for file in files:
            if file.endswith(".txt"):
                all_card_txt_files.append(os.path.join(root, file))

    from collections import Counter
    type_counter = Counter()

    for count, card_id in deck:
        for path in all_card_txt_files:
            if normalize(os.path.splitext(os.path.basename(path))[0]) == card_id:
                with open(path, "r", encoding="utf-8") as card_file:
                    for line in card_file:
                        if line.startswith("{category}"):
                            category = line.replace("{category}", "").strip()
                            type_counter[category] += count
                break

    if not type_counter:
        print("❌ No se encontraron tipos.")
        return

    plt.bar(type_counter.keys(), type_counter.values(), color='orange')
    plt.title("Distribución por Tipo de Carta")
    plt.ylabel("Cantidad")
    plt.tight_layout()
    plt.show()
