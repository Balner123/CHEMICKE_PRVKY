import csv
import json
from statistics import mean

# Načítání dat
def load_elements(file_path):
    """Načte data z CSV souboru a vrátí seznam prvků jako slovníky."""
    elements = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            elements = [row for row in reader]
    except FileNotFoundError:
        print("\nCSV soubor nenalezen.\n")
    return elements

def load_groups(file_path):
    """Načte data o skupinách z JSON souboru."""
    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            groups = json.load(jsonfile)
    except FileNotFoundError:
        print("\nJSON soubor nenalezen.\n")
        groups = {}
    return groups

# Hlavní menu a uživatelské rozhraní
def display_menu():
    """Zobrazí hlavní menu a nabídne uživateli volby."""
    
    message = """
    \n===================================================\n
                MENU - CHEMICKÉ PRVKY
    \n---------------------------------------------------\n
    1. Vyhledávání prvků
    2. Zobrazit vlastnosti prvku
    3. Výpočet průměrné atomové hmotnosti
    4. Generovat HTML soubor (přehled prvků)
    5. Exportovat data do JSON (vybrané prvky)
    6. Generovat Markdown přehled (skupina prvků)
    0. Ukončit
    \n===================================================\n
    """
    
    print(message)
    return input("Vyberte možnost: ")

def search_element(elements, groups, criterion, value):
    """Vyhledá prvek na základě daného kritéria a vrátí jeho vlastnosti."""
    for element in elements:
        if element.get(criterion) == value:
            print("\n--- Výsledek hledání ---")
            if not element.get("Group"):
                element["Group"] = find_group(groups, element["Symbol"])
            return element
    print("\nPrvek nebyl nalezen.\n")
    return {}

def find_group(groups, symbol):
    """Najde skupinu prvku podle jeho symbolu."""
    for group in groups:
        if symbol in group["elements"]:
            return group["cs"]
    return "Neznámá skupina"

def display_element(element):
    """Vypíše všechny vlastnosti zadaného prvku s lepším formátováním."""
    if element:
        print("\n--- Vlastnosti prvku ---")
        for key, value in element.items():
            print(f"{key: <20}: {value}")
        print("\n--- Konec výpisu ---\n")
    else:
        print("\nPrvek nenalezen.\n")

# Výpočet průměrné relativní atomové hmotnosti
def calculate_average_mass(elements, group=None, period=None):
    """Spočítá průměrnou relativní atomovou hmotnost prvků ve zvolené skupině NEBO periodě."""
    if group and period:
        print("\nChyba: Zadejte buď skupinu, nebo periodu, ne obojí.\n")
        return 0.0

    filtered_elements = []
    if group:
        filtered_elements = [float(element["AtomicMass"]) for element in elements if element["Group"] == group]
    elif period:
        filtered_elements = [float(element["AtomicMass"]) for element in elements if element["Period"] == period]
    else:
        print("\nMusíte zadat buď skupinu, nebo periodu.\n")
        return 0.0

    if filtered_elements:
        avg_mass = mean(filtered_elements)
        print(f"\nPrůměrná relativní atomová hmotnost: {avg_mass:.2f}\n")
        return avg_mass
    else:
        print("\nŽádné prvky k výpočtu pro dané kritérium.\n")
        return 0.0

# Generování výstupních souborů
def generate_html(elements, file_path="periodic_table.html"):
    """Vygeneruje HTML tabulku s přehledem všech prvků."""
    html_content = "<html>\n<body>\n<h1>Periodic Table of Elements</h1>\n<table border='1'>\n<tr>\n<th>Značka</th>\n<th>Název</th>\n<th>Protonové číslo</th>\n</tr>\n"
    for element in elements:
        html_content += f"<tr>\n<td>{element['Symbol']}</td>\n<td>{element['Element']}</td>\n<td>{element['AtomicNumber']}</td>\n</tr>"
    html_content += "</table></body></html>"
    
    with open(file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)
    print(f"\nHTML soubor '{file_path}' byl vygenerován.\n")

def export_to_json(elements, file_path="selected_elements.json"):
    """Umožní uživateli zadat více prvků pro export a uloží vybrané prvky do JSON souboru."""
    selected_symbols = []
    
    print("\nZadejte značky prvků, které chcete exportovat (prázdný vstup pro ukončení):")
    while True:
        symbol = input("Zadejte značku prvku: ").strip()
        if not symbol:  # Prázdný vstup ukončí zadávání
            break
        selected_symbols.append(symbol)

    # Filtrovat prvky podle zadaných značek
    selected_elements = [element for element in elements if element["Symbol"] in selected_symbols]
    
    # Uložit do JSON
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(selected_elements, json_file, ensure_ascii=False, indent=4)
    print(f"\nJSON soubor '{file_path}' byl úspěšně exportován s {len(selected_elements)} prvky.\n")

def generate_markdown(elements, file_path="group_overview.md"):
    """Vygeneruje Markdown soubor s přehledem prvků v konkrétní skupině nebo periodě."""
    md_content = "# Přehled chemických prvků\n\n"
    for element in elements:
        md_content += f"## {element['Symbol']} ({element['Element']})\n"
        md_content += f"- Protonové číslo: {element['AtomicNumber']}\n"
        md_content += f"- Relativní atomová hmotnost: {element['AtomicMass']}\n\n"
    
    with open(file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)
    print(f"\nMarkdown soubor '{file_path}' byl vygenerován.\n")

# Hlavní program
def main():
    elements = load_elements("elements.csv")
    groups = load_groups("groups.json")
    
    while True:
        choice = display_menu()
        
        if choice == '1':  # Vyhledávání prvků
            criterion = input("Zadejte kritérium (Symbol, Element (name), AtomicNumber, Group, Period): ")
            value = input(f"Zadejte hodnotu pro {criterion}: ")
            element = search_element(elements, groups, criterion, value)
            display_element(element)
        
        elif choice == '2':  # Zobrazit vlastnosti prvku
            symbol = input("Zadejte značku prvku: ")
            element = search_element(elements, groups, "Symbol", symbol)
            display_element(element)
        
        elif choice == '3':  # Výpočet průměrné hmotnosti
            group = input("Zadejte číslo skupiny (nebo prázdné, pokud chcete zadat periodu): ").strip()
            period = input("Zadejte číslo periody (nebo prázdné, pokud jste zadali skupinu): ").strip()
            
            # Předání hodnoty pouze jednoho kritéria do funkce
            if group and period:
                print("\nZadejte buď skupinu, nebo periodu, ne obojí.\n")
            elif group:
                calculate_average_mass(elements, group=group)
            elif period:
                calculate_average_mass(elements, period=period)
            else:
                print("\nMusíte zadat buď skupinu, nebo periodu.\n")
        
        elif choice == '4':  # Generovat HTML
            generate_html(elements)
        
        elif choice == '5':  # Export do JSON
            export_to_json(elements)
        
        elif choice == '6':  # Generovat Markdown
            group = input("Zadejte skupinu: ")
            selected_elements = [element for element in elements if element["Group"] == group]
            generate_markdown(selected_elements)
        
        elif choice == '0':  # Ukončit program
            print("\nUkončuji program.\n")
            break
        else:
            print("\nNeplatná volba, zkuste to znovu.\n")
        
        input("Stiskněte Enter pro pokračování...")

if __name__ == "__main__":
    main()