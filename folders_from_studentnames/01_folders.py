import csv
import os


def create_folder(foldername):
    my_path = 'C://Users/jonasha/Downloads/'
    try:
        os.makedirs(my_path + foldername)
    except OSError:
        pass
    os.chdir(my_path + foldername)

create_folder("000_DesignStudio_HS_0000")
create_folder("000_DesignStudio_HS_0000/00 Grundlagen")
create_folder("000_DesignStudio_HS_0000/01 Abgaben")
create_folder("000_DesignStudio_HS_0000/01 Abgaben/01 Vorübung")
create_folder("000_DesignStudio_HS_0000/02 Workspace Studierende")

with open('C://Users/jonasha/Downloads/liste.csv', encoding="utf8") as file_obj:
    reader_obj = csv.reader(file_obj)
    usernames = []

    for row in reader_obj:
        folder_path = "000_DesignStudio_HS_0000/01 Abgaben/01 Vorübung/" + str(row[1] + " " + str(row[0]))
        create_folder(folder_path)
    