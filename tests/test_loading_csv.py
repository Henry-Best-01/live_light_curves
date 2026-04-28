import csv


file_name_csv = "./sample_csv_lenses.csv"

current_targets = []
with open(file_name_csv, 'r') as f:
    my_reader = csv.DictReader(f)
    for row in my_reader:
        current_targets.append(row)

print(current_targets)
