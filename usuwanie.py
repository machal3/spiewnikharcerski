import os

def czyszczenie_folderu(sciezka_do_folderu):
    # Sprawdzenie, czy folder istnieje
    if not os.path.exists(sciezka_do_folderu):
        print(f"Błąd: Folder '{sciezka_do_folderu}' nie istnieje.")
        return

    print(f"Rozpoczynam czyszczenie folderu: {sciezka_do_folderu}...")

    # Iteracja przez wszystkie pliki w folderze
    for plik in os.listdir(sciezka_do_folderu):
        pelna_sciezka = os.path.join(sciezka_do_folderu, plik)

        # Upewniamy się, że to plik, a nie podfolder
        if os.path.isfile(pelna_sciezka):
            # Rozdzielamy nazwę pliku i rozszerzenie
            nazwa_pliku, rozszerzenie = os.path.splitext(plik)

            # Sprawdzamy, czy nazwa NIE kończy się na "_H"
            if not nazwa_pliku.endswith("_H"):
                try:
                    os.remove(pelna_sciezka)
                    print(f"Usunięto: {plik}")
                except Exception as e:
                    print(f"Nie udało się usunąć {plik}. Błąd: {e}")
            else:
                print(f"Zachowano: {plik}")

if __name__ == "__main__":
    # Tutaj wpisz nazwę swojego folderu lub pełną ścieżkę do niego
    folder = "Folder"
    
    czyszczenie_folderu(folder)