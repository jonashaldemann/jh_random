import os

def rename_files_in_directory(directory, old_string, new_string):
    try:
        # Überprüfen, ob das Verzeichnis existiert
        if not os.path.isdir(directory):
            print(f"Das Verzeichnis '{directory}' existiert nicht.")
            return

        # Alle Dateien im Verzeichnis durchgehen
        for filename in os.listdir(directory):
            old_file_path = os.path.join(directory, filename)

            # Nur Dateien berücksichtigen
            if os.path.isfile(old_file_path):
                # Prüfen, ob die alte Zeichenkette im Dateinamen vorkommt
                if old_string in filename:
                    # Neuer Dateiname
                    new_filename = filename.replace(old_string, new_string)
                    new_file_path = os.path.join(directory, new_filename)

                    # Datei umbenennen
                    os.rename(old_file_path, new_file_path)
                    print(f"'{filename}' umbenannt in '{new_filename}'")
                else:
                    print(f"'{filename}' enthält nicht die Zeichenkette '{old_string}' und wird übersprungen.")

        print("Alle Dateien wurden verarbeitet.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Beispielaufruf
if __name__ == "__main__":
    # Verzeichnis, alte und neue Zeichenkette
    directory = input("Gib den Pfad zum Verzeichnis ein: ").strip()
    old_string = input("Gib den Ursprungsnamen ein: ").strip()
    new_string = input("Gib den Zielnamen ein: ").strip()

    # Funktion aufrufen
    rename_files_in_directory(directory, old_string, new_string)