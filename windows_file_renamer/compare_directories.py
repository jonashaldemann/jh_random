import os
import csv

def compare_directories(source_dir, target_dir, output_file):
    try:
        # Überprüfen, ob die Verzeichnisse existieren
        if not os.path.isdir(source_dir):
            print(f"Das Quellverzeichnis '{source_dir}' existiert nicht.")
            return

        if not os.path.isdir(target_dir):
            print(f"Das Zielverzeichnis '{target_dir}' existiert nicht.")
            return

        # Alle Dateien im Quellverzeichnis (nur Dateinamen sammeln, keine Pfade)
        source_files = {}
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file not in source_files:
                    source_files[file] = os.path.join(root, file)

        # Alle Dateien im Zielverzeichnis (nur Dateinamen sammeln, keine Pfade)
        target_files = set()
        for root, _, files in os.walk(target_dir):
            for file in files:
                target_files.add(file)

        # Dateien finden, die im Zielverzeichnis fehlen
        missing_files = [file for file in source_files if file not in target_files]

        # Ergebnis in eine CSV-Datei schreiben
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';')
            # Header schreiben
            csvwriter.writerow(["Dateiname", "Quellpfad"])

            # Fehlende Dateien eintragen
            for file in missing_files:
                csvwriter.writerow([file, source_files[file]])

        print(f"Der Vergleich wurde abgeschlossen. Ergebnisse wurden in '{output_file}' gespeichert.")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Beispielaufruf
if __name__ == "__main__":
    source_dir = input("Gib das Quellverzeichnis ein: ").strip()
    target_dir = input("Gib das Zielverzeichnis ein: ").strip()
    output_file = r"C:\Users\jonasha\Desktop\missing_files.csv"

    compare_directories(source_dir, target_dir, output_file)