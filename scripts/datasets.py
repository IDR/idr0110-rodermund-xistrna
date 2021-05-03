import csv

"""
Get the right dataset - image mapping from the assays file
"""

assays_file = "../experimentA/idr0000-lisa-rodermund-assays.txt"
filepaths_file = "../experimentA/idr0110-experimentA-filePaths.tsv"

dataset_map = {}
with open(assays_file, newline='') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        dataset_map[row[1]] = row[0]


with open(filepaths_file, newline='') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        path = row[1]
        img = row[2]
        ds = dataset_map[img]
        print(f"Project:name:idr0110-rodermund-xistrna/experimentA/Dataset:name:{ds}\t{path}\t{img}")
