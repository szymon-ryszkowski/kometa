import csv
_data = []
file_path = "./Sun_data/composite_lyman_alpha.csv"
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        value = float(row[1])
        _data.append(value)

def sun_aktywnosc (dzien):
    return (_data[dzien] - 0.0061) / 0.0037




