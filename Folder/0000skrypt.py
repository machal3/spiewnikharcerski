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
    sample_text = """Ballada o spalonej synagodze
Żydzi, Żydzi wstawajcie płonie synagoga!	a G a
Cała Wschodnia Ściana porosła już żarem!	a G a
Powietrze drży, skacze po suchych belkach ogień!	a G a
Wstawajcie, chrońcie święte księgi wiary!	a G e a

Gromadzą się ciemni w krąg płonącego gmachu,	a G a
Biegają iskry po pejsach, tlą się długie brody,	a G C
W oczach blask pożaru, rozpaczy i strachu –	d C d a
Gdzie będą teraz wznosić swoje próżne modły?!	a G e a

Płonie synagoga! Trzask i krzyk gardłowy!	a G a
Belki w żar się sypią, iskry w górę lecą!	a G a
Tam, w środku Żyd został! Jeszcze widać ręce!	a G a
Już czarne! O, Jehowo, za co? O, Jehowo?!	a G e a

Noc zapadła. Stoją wszyscy wielkim kołem,	a G a
Chmury nisko, w ciemnościach gwiazda się dopala.	a G C
Patrzą na swe chałaty porosłe popiołem,	d C d a
Rząd rąk i twarzy w mrok się powoli oddala…	a G e a

Stali tak do rana, deszcz spadł, ciągle stali	a d
Aż popiół się zmieszał ze szlamem.	d a
– Jeden Żyd się spalił! Jeden Żyd się spalił!	a
Śpiewał w knajpie nad wódką włóczęga pijany.	d e a
"""
    format_song_to_file(sample_text)