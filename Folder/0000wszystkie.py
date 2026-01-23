import os

def migrate_to_longtable():
    folder_path = os.getcwd()
    files = [f for f in os.listdir(folder_path) if f.endswith('.tex')]
    
    print(f"Rozpoczynam migrację {len(files)} plików do longtable{{ll}}...")

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Jeśli plik już ma nowy format, pomiń
        if "\\begin{longtable}{ll}" in content:
            continue

        lines = content.splitlines()
        new_lines = []
        table_start = "\\begin{longtable}{ll}"
        table_end = "\\end{longtable}"
        is_table_open = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("\\section"):
                new_lines.append(line)
                new_lines.append(table_start)
                is_table_open = True
                continue
                
            if line.startswith("\\begin{tabular}") or line.startswith("\\end{tabular}"):
                continue
                
            if line == r"\\":
                new_lines.append(r" & \\")
                continue
                
            if line == r"\newpage":
                if is_table_open:
                    new_lines.append(table_end)
                new_lines.append(r"\newpage")
                new_lines.append(table_start)
                is_table_open = True
                continue
            
            if line.endswith(r"\\"):
                # Usuwanie pustych \textbf{} jeśli się trafią
                processed_line = line.replace("\\textbf{}", "")
                if "&" not in processed_line:
                    processed_line = processed_line[:-2] + " & \\\\"
                new_lines.append(processed_line)

        if is_table_open:
            new_lines.append(table_end)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(new_lines))
        print(f"Przerobiono: {filename}")

if __name__ == "__main__":
    migrate_to_longtable()