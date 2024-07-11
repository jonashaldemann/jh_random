import csv
import os


def create_folder(foldername):
    my_path = 'C://Users/jonasha/Downloads/'
    try:
        os.makedirs(my_path + foldername)
    except OSError:
        pass
    os.chdir(my_path + foldername)

create_folder("02 Konzeptbesprechung")
create_folder("03 Zwischenbesprechung")
create_folder("04 Praesentationsbesprechung")
create_folder("05 Schlussbesprechung")

with open('C://Users/jonasha/Downloads/liste.csv', encoding="utf8") as file_obj:
    reader_obj = csv.reader(file_obj)
    usernames = []
    for row in reader_obj:
        usernames.append(row[2])

    teams = []
    team = ""
    for i in range(len(usernames)):
        if i % 2 == 0:
            team = str(usernames[i]) + "_"
        else:
            team = team + str(usernames[i])
            teams.append(team)

    for i in teams:
        folder_path = "02 Konzeptbesprechung/" + str(i)
        create_folder(folder_path)

        folder_path = "03 Zwischenbesprechung/" + str(i)
        create_folder(folder_path)

        folder_path = "04 Praesentationsbesprechung/" + str(i)
        create_folder(folder_path)

        folder_path = "05 Schlussbesprechung/" + str(i)
        create_folder(folder_path)
