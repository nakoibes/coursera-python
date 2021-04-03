import csv
raw_data = []
with open('cars.csv') as csv_fd:
    reader = csv.reader(csv_fd, delimiter=';')
    next(reader)
    for car in reader:
        raw_data.append(car)
        print(car)