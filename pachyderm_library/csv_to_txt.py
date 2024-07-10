import csv

csv_file_path = "pachyderm_library.csv"

with open(csv_file_path, mode="r", newline="") as file:
    csv_reader = csv_reader(file)