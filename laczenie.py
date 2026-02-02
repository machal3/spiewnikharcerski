import os

# --- KONFIGURACJA ---
# Lista folderów do przeszukania (kolejność na liście decyduje o kolejności w pliku wynikowym)
source_folders = ["Folder stałe", "Folder"]

# Nazwa pliku wynikowego
output_filename = "spiewnikharcerski.tex"

def merge_tex_files():
    # Lista, w której zgromadzimy pełne ścieżki do wszystkich plików
    all_files_to_merge = []

    # 1. Zbieranie plików z obu folderów
    print("--- Rozpoczynam indeksowanie plików ---")
    
    for folder in source_folders:
        if not os.path.exists(folder):
            print(f"OSTRZEŻENIE: Folder '{folder}' nie istnieje! Pomijam go.")
            continue

        # Pobierz pliki .tex i posortuj je alfabetycznie wewnątrz danego folderu
        files = [f for f in os.listdir(folder) if f.endswith(".tex")]
        files.sort()

        if not files:
            print(f"Info: Folder '{folder}' jest pusty (brak plików .tex).")
        else:
            print(f"Z folderu '{folder}' dodano {len(files)} plików.")
            # Dodajemy pełne ścieżki do głównej listy
            for filename in files:
                full_path = os.path.join(folder, filename)
                all_files_to_merge.append(full_path)

    # Sprawdzenie czy w ogóle mamy co łączyć
    if not all_files_to_merge:
        print("\nBŁĄD: Nie znaleziono żadnych plików .tex w podanych folderach.")
        return

    print(f"\nŁącznie do przetworzenia: {len(all_files_to_merge)} plików. Zapisywanie...")

    # 2. Łączenie plików w jeden wynikowy
    with open(output_filename, "w", encoding="utf-8") as outfile:
        outfile.write("% Ten plik został wygenerowany automatycznie.\n")
        
        for i, file_path in enumerate(all_files_to_merge):
            print(f"Przetwarzanie: {file_path}")
            
            try:
                with open(file_path, "r", encoding="utf-8") as infile:
                    content = infile.read()
                    
                    # Dodaj nagłówek komentarza z nazwą pliku
                    outfile.write(f"\n% --- Źródło: {file_path} ---\n")
                    
                    # Wpisz treść
                    outfile.write(content)
                    
                    # Dodaj podział strony (jeśli to NIE jest ostatni plik na liście)
                    if i < len(all_files_to_merge) - 1:
                        outfile.write("\n\\clearpage\n")
            
            except Exception as e:
                print(f"BŁĄD przy odczycie pliku {file_path}: {e}")

    print(f"\nGotowe! Wszystkie piosenki zostały połączone w pliku: {output_filename}")

if __name__ == "__main__":
    merge_tex_files()