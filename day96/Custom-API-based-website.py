import requests

BASE_URL = "https://hp-api.onrender.com/api/characters"

def get_all_characters():
    """Fetch all characters from the API."""
    try:
        response = requests.get(BASE_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []

def get_characters_by_house(house):
    """Fetch characters by Hogwarts house."""
    try:
        url = f"{BASE_URL}/house/{house.lower()}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []

def search_character_by_name(name):
    """Search for characters by name."""
    all_chars = get_all_characters()
    name = name.lower().strip()
    return [char for char in all_chars if name in char.get("name", "").lower()]

def display_characters(characters, limit=10):
    """Display characters neatly."""
    if not characters:
        print("No characters found.")
        return
    for i, c in enumerate(characters[:limit], start=1):
        print(f"\n[{i}] {c.get('name', 'Unknown')}")
        print("House:", c.get('house', 'Unknown'))
        print("Species:", c.get('species', 'Unknown'))
        print("Ancestry:", c.get('ancestry', 'Unknown'))
        print("Actor:", c.get('actor', 'Unknown'))
        print("Image URL:", c.get('image', 'No image'))
    if len(characters) > limit:
        print(f"\n...and {len(characters) - limit} more results.")

def main():
    print("=== Harry Potter Character Explorer ===")
    print("1. View all characters (first 20)")
    print("2. View characters by house")
    print("3. Search characters by name")
    print("4. Exit")

    while True:
        choice = input("\nEnter choice (1/2/3/4): ").strip()
        if choice == "1":
            chars = get_all_characters()
            display_characters(chars, limit=20)
        elif choice == "2":
            house = input("Enter house (gryffindor / slytherin / hufflepuff / ravenclaw): ").strip()
            chars = get_characters_by_house(house)
            display_characters(chars, limit=20)
        elif choice == "3":
            name = input("Enter name to search: ").strip()
            chars = search_character_by_name(name)
            display_characters(chars, limit=20)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
