import csv
import os


def create_folder(foldername):
    my_path = 'C://Users/jonasha/Downloads/'
    try:
        os.makedirs(my_path + foldername)
    except OSError:
        pass
    os.chdir(my_path + foldername)

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

subfolder_file = open(r"C:\Users\jonasha\Documents\Repositories\pythontools\folders_from_names\subfolders.txt")
subfolder_lines = subfolder_file.readlines()
print(subfolder_lines)

for subfolder in subfolder_lines:
    folder_path = subfolder[:-1]
    for team in teams:
        folder_path = folder_path.replace("TEAM", team)
        print(folder_path)
        create_folder(folder_path)

