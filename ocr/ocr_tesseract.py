from pathlib import Path
import subprocess

folder = Path("/Users/jonashaldemann/Downloads")

for pdf in folder.glob("*.pdf"):
    subprocess.run([
        "ocrmypdf",
        "--language", "deu+eng",
        "--skip-text",
        "--rotate-pages",
        "--deskew",
        str(pdf),
        str(pdf.with_stem(pdf.stem + "_ocr"))
    ])