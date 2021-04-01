import csv
import os


class CarBase:
    def __init__(self, car_type, photo_file_name, brand, carrying):
        self.car_type = car_type
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = carrying

    def get_photo_file_ext(self):
        return self.get_photo_file_ext()

    def _get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)


class Car(CarBase):
    def __init__(self, car_type=None, photo_file_name=None, brand=None, carrying=None, passenger_seats_count=None):
        super(Car, self).__init__(car_type, photo_file_name, brand, carrying)
        self.passenger_seats_count = passenger_seats_count


class Truck(CarBase):
    def __init__(self, car_type=None, photo_file_name=None, brand=None, carrying=None, body_whl='0x0x0'):
        super(Truck, self).__init__(car_type, photo_file_name, brand, carrying)
        self.body_length, self.body_width, self.body_height = self._initialize(body_whl)

    def get_body_volume(self):
        return self._get_body_volume()

    def _get_body_volume(self):
        return int(self.body_length) * int(self.body_width) * int(self.body_height)

    @staticmethod
    def _initialize(body_whl):
        return body_whl.split('x')


class SpecMachine(CarBase):
    def __init__(self, car_type=None, photo_file_name=None, brand=None, carrying=None, extra=None):
        super(SpecMachine, self).__init__(car_type, photo_file_name, brand, carrying)
        self.extra = extra


def isvalid(data):
    if data[0] == '':
        return False
    return True


def make_object(row):
    if row[0] == 'car':
        return Car(row[0], row[3], row[1], row[5], row[2])
    elif row[0] == 'truck':
        return Truck(row[0], row[3], row[1], row[5], row[4])
    else:
        return SpecMachine(row[0], row[3], row[1], row[5], row[6])


def get_car_list(file_name):
    list_objects = []
    with open(file_name) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)
        for row in reader:
            if (row != []) and isvalid(row):
                list_objects.append(make_object(row))
                #print(row)
    return list_objects


def main():
    get_car_list('cars.csv')


if __name__ == '__main__':
    main()
