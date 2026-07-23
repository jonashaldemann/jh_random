import csv
from datetime import datetime
import os

# ==========================
# Konfiguration
# ==========================

# Ordner mit den Report-Dateien
FOLDER_PATH = "/Users/jonashaldemann/Downloads"

# Name der Ausgabedatei
OUTPUT_FILENAME = "Report_excel_ready.csv"

# Spalte, die als Datum verwendet wird
DATE_COLUMN = "start"

# Diese Spalten werden entfernt
REMOVE_COLUMNS = [
    "end",
    "status",
    "client",
    "project",
    # "note",
    # "duration",
    # "task",
    # "author",
]

# ==========================
# Programm
# ==========================

# Neueste Datei finden, die mit "Report_" beginnt
report_files = [
    f for f in os.listdir(FOLDER_PATH)
    if f.startswith("Report_") and f.endswith(".csv")
]

if not report_files:
    raise FileNotFoundError("⚠️ Keine Datei mit 'Report_' im Namen gefunden.")

report_files.sort(
    key=lambda f: os.path.getmtime(os.path.join(FOLDER_PATH, f)),
    reverse=True,
)

input_file = os.path.join(FOLDER_PATH, report_files[0])
output_file = os.path.join(FOLDER_PATH, OUTPUT_FILENAME)

# Öffnen und schreiben
with open(input_file, mode="r", encoding="utf-8", newline="") as infile, \
     open(output_file, mode="w", encoding="utf-8-sig", newline="") as outfile:

    reader = csv.reader(infile, delimiter=",")
    writer = csv.writer(outfile, delimiter=";")

    header = next(reader)

    # Indizes bestimmen
    index_start = header.index(DATE_COLUMN)
    remove_indices = {header.index(col) for col in REMOVE_COLUMNS}

    # Neue Kopfzeile
    new_header = [
        "datum"
    ] + [
        h for i, h in enumerate(header)
        if i != index_start and i not in remove_indices
    ]
    writer.writerow(new_header)

    for row in reader:
        # Datum umformatieren
        try:
            datum = datetime.strptime(
                row[index_start], "%Y-%m-%d %H:%M:%S"
            ).strftime("%d.%m.%Y")
        except ValueError:
            datum = row[index_start]

        # Neue Zeile schreiben
        new_row = [
            datum
        ] + [
            cell for i, cell in enumerate(row)
            if i != index_start and i not in remove_indices
        ]
        writer.writerow(new_row)

print(f"✅ Datei verarbeitet: {input_file}")
print(f"📄 Neue Datei gespeichert als: {output_file}")