# Śpiewnik

Ten projekt to zautomatyzowany śpiewnik oparty na systemie **LaTeX**. Umożliwia łatwe zarządzanie bazą piosenek poprzez przechowywanie każdego utworu w oddzielnym pliku i automatyczne łączenie ich w jeden dokument gotowy do druku.

## 📂 Struktura projektu

* **`Folder/`** – Katalog zawierający pliki źródłowe `.tex`. Znajdują się tu:
  * `000poczontek.tex` – Początek dokumentu (strona tytułowa, spis treści).
  * `Pliki z piosenkami` – Pojedyncze pliki `.tex` z tekstami i chwytami.
  * `ŻŻŻŻkoniec.tex` – Zakończenie dokumentu.
* **`laczenie`** – Skrypt w języku Python, który łączy zawartość katalogu `Folder/` w jedną całość.
* **`spiewnikpelny.tex`** – Główny plik wynikowy do kompilacji.

## 🚀 Jak dodać nową piosenkę?

Aby dodać nowy utwór do śpiewnika, wykonaj następujące kroki:

### 1. Utwórz nowy plik
W katalogu `Folder/` stwórz nowy plik tekstowy z rozszerzeniem `.tex`. Nazwij go tytułem piosenki (np. `Tytul_Piosenki.tex`). Pamiętaj, że skrypt łączy pliki w kolejności alfabetycznej.

### 2. Wklej szablon
Skopiuj poniższy kod do swojego nowego pliku i uzupełnij go tekstem oraz chwytami:

```latex
\section{Tytuł Piosenki}
\vspace{-\baselineskip}
\textit{Autor / Wykonawca}\\
\begin{longtable}{ll}
Pierwsza linijka tekstu & \textbf{a C G} \\
Druga linijka tekstu & \textbf{d E a} \\
& \\
\hspace*{2em}\textit{Treść refrenu} & \textbf{C G} \\
\hspace*{2em}\textit{Druga linijka refrenu} & \textbf{a E} \\
& \\
Kolejna zwrotka... & \textbf{a C} \\
\end{longtable}
```
Możesz użyć też skryptu ```0000skrypt.py```. Wklej pod koniec tekst piosenki w następujący sposób
- w pierwszej linijce daj tytuł piosenki
- każdy wiersz w innym wierszu.
- po tabulatorze w każdym wierszu napisz chwyty
- przy refrenie daj tabulator na początku wiersza

Poniżej skrypt ```0000skrypt.py```
```
import re

def format_song_to_file(text):
    """
    Przekształca tekst piosenki na format LaTeX w środowisku longtable.
    Obie kolumny wyrównane do lewej {ll}.
    """
    lines = text.splitlines()
    result = []
    is_first_line = True
    empty_lines_count = 0
    
    # Nagłówek i stopka tabeli (ll = lewa, lewa)
    table_start = "\\begin{longtable}{ll}"
    table_end = "\\end{longtable}"

    title = lines[0].strip() if lines else "Piosenka"
    safe_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '_')
    filename = f"{safe_title}.tex"

    is_table_open = False

    for line in lines:
        stripped_line = line.strip()

        # --- OBSŁUGA PUSTYCH LINII ---
        if stripped_line == "":
            empty_lines_count += 1
            if is_table_open and empty_lines_count == 1:
                result.append(" & \\\\") 
            if empty_lines_count == 2:
                if is_table_open:
                    result.append(table_end)
                    is_table_open = False
                result.append("\\newpage")
            continue
        else:
            empty_lines_count = 0 

        # --- OBSŁUGA TYTUŁU ---
        if is_first_line:
            result.append(f"\\section{{{stripped_line}}}")
            result.append(table_start)
            is_table_open = True
            is_first_line = False
            continue

        if not is_table_open:
            result.append(table_start)
            is_table_open = True

        # --- FORMATOWANIE WIERSZY ---
        if line.startswith("\t"):
            line_content = line.lstrip("\t")
            if "\t" in line_content:
                parts = line_content.split("\t", 1)
                text_part = parts[0].strip()
                chords_part = parts[1].strip()
                # Wstawiamy \textbf tylko jeśli chwyt nie jest pusty
                chord_str = f"\\textbf{{{chords_part}}}" if chords_part else ""
                formatted_line = f"\\hspace*{{2em}}\\textit{{{text_part}}} & {chord_str} \\\\"
            else:
                formatted_line = f"\\hspace*{{2em}}\\textit{{{line_content}}} & \\\\"
            result.append(formatted_line)

        elif "\t" in line:
            parts = line.split("\t", 1)
            lyric = parts[0].rstrip()
            chords = parts[1].strip()
            chord_str = f"\\textbf{{{chords}}}" if chords else ""
            formatted_line = f"{lyric} & {chord_str} \\\\"
            result.append(formatted_line)

        else:
            formatted_line = f"{stripped_line} & \\\\"
            result.append(formatted_line)

    if is_table_open:
        result.append(table_end)

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(result))
    print(f"Zapisano: {filename}")

if __name__ == "__main__":
    sample_text = """Tytuł
Wers 1	a G a
Wers 2	a G a
Wers 3	a G a
Wers 4	a G e a


"""
    format_song_to_file(sample_text)
```
Następnie uruchom skrypt, a pliki `.tex` sam się utworzy. Autora musisz samemu dodać
### 3. Zaktualizuj śpiewnik

Uruchom skrypt, aby dodać nowy plik do głównego dokumentu:
```
python laczenie.py
```

### 4. Wygeneruj PDF

Otwórz plik spiewnikpelny.tex i skompiluj go w swoim edytorze LaTeX (np. używając pdflatex).

## 🛠 Wymagania
- Python 3 (do uruchomienia skryptu łączącego).
- Środowisko LaTeX (do kompilacji pliku PDF).
