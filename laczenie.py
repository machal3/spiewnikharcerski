import os

# --- KONFIGURACJA ---
# Nazwa folderu, w którym trzymasz pliki .tex
source_folder = "Folder"
# Nazwa pliku wynikowego (zostanie utworzony obok skryptu)
output_filename = "spiewnikharcerski.tex"

def merge_tex_files():
    # 1. Sprawdź, czy folder w ogóle istnieje
    if not os.path.exists(source_folder):
        print(f"BŁĄD: Nie znaleziono folderu o nazwie '{source_folder}'.")
        print("Upewnij się, że skrypt leży OBOK tego folderu.")
        return

    # 2. Pobierz listę plików .tex z wnętrza folderu
    files = [f for f in os.listdir(source_folder) if f.endswith(".tex")]
    
    # Sortuj alfabetycznie
    files.sort()

    if not files:
        print(f"W folderze '{source_folder}' nie ma żadnych plików .tex!")
        return

    print(f"Znaleziono {len(files)} plików w folderze '{source_folder}'. Rozpoczynam łączenie...")

    # 3. Otwórz plik wynikowy do zapisu
    with open(output_filename, "w", encoding="utf-8") as outfile:
        outfile.write("% Ten plik został wygenerowany automatycznie.\n")
        
        for i, filename in enumerate(files):
            # Pełna ścieżka do pliku (Folder/plik.tex)
            file_path = os.path.join(source_folder, filename)
            
            print(f"Przetwarzanie: {filename}")
            
            with open(file_path, "r", encoding="utf-8") as infile:
                content = infile.read()
                
                # Dodaj nagłówek komentarza, żebyś wiedział, skąd pochodzi fragment
                outfile.write(f"\n% --- Źródło: {filename} ---\n")
                
                # Wpisz treść
                outfile.write(content)
                
                # Dodaj podział strony (oprócz ostatniego pliku)
                if i < len(files) - 1:
                    outfile.write("\n\\clearpage\n")

    print(f"\nGotowe! Wszystkie piosenki zostały połączone w pliku: {output_filename}")

if __name__ == "__main__":
    merge_tex_files()