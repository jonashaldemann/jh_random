import os

# Projektliste lesen, neue Projektnummer
file_projectlist = open("/Users/jonashaldemann/Nextcloud2/Büro/000 Admin/Projektliste/Projektliste.txt", "r+")
projects = file_projectlist.readlines()
last_project = projects[-1:][0]
last_project_number = int(last_project.split(" ")[0])
new_project_number = str(last_project_number + 1)

# Neues Projekt definieren
pr_number = new_project_number.zfill(3)
pr_name = input("Projektname:")

# Projektordner definieren
main_folder = "/Users/jonashaldemann/Nextcloud2/Büro/" + pr_number + " " + pr_name

# Hauptordner kreieren
try:
    os.mkdir(main_folder)
except OSError:
    print("Creation of the directory %s failed" % main_folder)

# Unterordner kreieren
file_subfolders = open("/Users/jonashaldemann/Documents/Repositories/jh_random/hv_projectfolder/Subfolders.txt", "r")
subfolders = file_subfolders.readlines()

for sub_folder in subfolders:
    try:
        os.mkdir(main_folder + "/" + sub_folder[:-1])
    except OSError:
        print("Creation of the directory %s failed" % sub_folder)

# Projektliste nachtragen
file_projectlist.write(pr_number + " " + pr_name + "\n")

file_projectlist.close()
file_subfolders.close()
