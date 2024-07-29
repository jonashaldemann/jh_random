import csv

rows = []

with open("jh_random\pachyderm_library\pachyderm_library.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        text = row[0]
        cells = text.split(";")
        
        for i in range(len(cells)):
            if len(cells[i]) == 1:
                cells[i] = "0" + cells[i]
            else:
                pass
        
        string = ""
        for i in range(len(cells)):
            if i == 0:
                string += str(cells[i])
                string += ":"
            else:
                string += str(cells[i])
        
        rows.append(string)

file.close()

rows = rows[1:]

textfile = open("jh_random\pachyderm_library\Pach_Materials_Library.txt", "w")
for row in rows:
    textfile.write(row)
    textfile.write("\n")

textfile.close()

