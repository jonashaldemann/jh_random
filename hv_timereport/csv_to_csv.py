import csv
from datetime import datetime
import os

# Ordner mit den Report-Dateien
folder_path = "/Users/jonashaldemann/Downloads"

# Neueste Datei finden, die mit "Report_" beginnt
report_files = [f for f in os.listdir(folder_path) if f.startswith("Report_") and f.endswith(".csv")]
if not report_files:
    raise FileNotFoundError("⚠️ Keine Datei mit 'Report_' im Namen gefunden.")

report_files.sort(key=lambda f: os.path.getmtime(os.path.join(folder_path, f)), reverse=True)
input_file = os.path.join(folder_path, report_files[0])
output_file = os.path.join(folder_path, "Report_excel_ready.csv")

# Öffnen und schreiben
with open(input_file, mode="r", encoding="utf-8", newline="") as infile, \
     open(output_file, mode="w", encoding="utf-8-sig", newline="") as outfile:  # utf-8 with BOM!

    reader = csv.reader(infile, delimiter=",")
    writer = csv.writer(outfile, delimiter=";")

    header = next(reader)

    # Indizes bestimmen
    index_start = header.index("start")
    index_status = header.index("status")
    index_end = header.index("end")

    # Neue Kopfzeile: "datum" statt "start", "end" & "status" entfernt
    new_header = ["datum"] + [h for i, h in enumerate(header) if i not in (index_end, index_status, index_start)]
    writer.writerow(new_header)

    for row in reader:
        try:
            datum = datetime.strptime(row[index_start], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y")
        except ValueError:
            datum = row[index_start]

        new_row = [datum] + [cell for i, cell in enumerate(row) if i not in (index_end, index_status, index_start)]
        writer.writerow(new_row)

print(f"✅ Datei verarbeitet: {input_file}")
print(f"📄 Neue Datei gespeichert als: {output_file}")
