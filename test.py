import os

print("Current Working Directory:")
print(os.getcwd())

print("\nCards Folder Listing:")
cards_path = os.path.join(os.getcwd(), "Cards")
for root, dirs, files in os.walk(cards_path):
    for file in files:
        if file.endswith(".txt"):
            print(os.path.join(root, file))
