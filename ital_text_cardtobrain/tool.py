import re
import json
import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "italienisch.txt"
OUTPUT_FILE = BASE_DIR / "italienisch_plus.txt"

KNOWN_WORDS_FILE = BASE_DIR / "bekannte_woerter.json"
TRANSLATED_WORDS_FILE = BASE_DIR / "uebersetzte_woerter.json"

CSV_FILE = BASE_DIR / "vokabeln.csv"


def load_json_set(path: Path):
    if not path.exists():
        return set()

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return set(data)


def save_json_set(path: Path, data_set: set):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sorted(data_set), f, ensure_ascii=False, indent=2)


def tokenize(text):
    return re.findall(r"\w+|[^\w\s]|\s+", text, re.UNICODE)


def is_word(token):
    return re.fullmatch(r"\w+", token, re.UNICODE) is not None


def get_next_csv_index():
    if not CSV_FILE.exists():
        return 1

    existing_files = list(BASE_DIR.glob("vokabeln_*.csv"))

    max_index = 0

    for file in existing_files:
        match = re.search(r"vokabeln_(\d+)\.csv", file.name)
        if match:
            max_index = max(max_index, int(match.group(1)))

    return max_index + 1


def write_csv(rows, file_index):
    filename = BASE_DIR / f"vokabeln_{file_index:03d}.csv"

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Italienisch", "Deutsch", "Antworttyp"])

        for row in rows:
            writer.writerow([row[0], row[1], "text"])

    return filename


def main():
    if not INPUT_FILE.exists():
        print(f"Datei nicht gefunden: {INPUT_FILE}")
        return

    text = INPUT_FILE.read_text(encoding="utf-8")

    known_words = load_json_set(KNOWN_WORDS_FILE)
    translated_words = load_json_set(TRANSLATED_WORDS_FILE)

    asked_words = {}
    csv_rows = []

    tokens = tokenize(text)

    for token in tokens:
        if not is_word(token):
            continue

        lower = token.lower()

        if lower in known_words:
            continue

        if lower in translated_words:
            continue

        if lower in asked_words:
            continue

        print()
        print(f"Wort: {token}")

        answer = input("Kennst du das Wort? (y/n): ").strip().lower()

        if answer == "y":
            known_words.add(lower)
            asked_words[lower] = None

        else:
            translation = input("Deutsche Übersetzung: ").strip()

            asked_words[lower] = translation

            csv_rows.append([token, translation])

            translated_words.add(lower)

    output_tokens = []

    for token in tokens:
        if not is_word(token):
            output_tokens.append(token)
            continue

        lower = token.lower()

        if lower in asked_words and asked_words[lower]:
            output_tokens.append(f"{token} ({asked_words[lower]})")
        else:
            output_tokens.append(token)

    OUTPUT_FILE.write_text("".join(output_tokens), encoding="utf-8")

    save_json_set(KNOWN_WORDS_FILE, known_words)
    save_json_set(TRANSLATED_WORDS_FILE, translated_words)

    if csv_rows:
        file_index = get_next_csv_index()
        csv_file = write_csv(csv_rows, file_index)

        print(f"CSV: {csv_file}")

    print()
    print("Fertig.")
    print(f"Text: {OUTPUT_FILE}")
    print(f"Bekannte Wörter: {KNOWN_WORDS_FILE}")
    print(f"Übersetzte Wörter: {TRANSLATED_WORDS_FILE}")


if __name__ == "__main__":
    main()