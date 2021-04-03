import csv
import os


class CarBase:
    def __init__(self, car_type, photo_file_name, brand, carrying):
        self.car_type = car_type
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = carrying

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    def __init__(self, brand=None, photo_file_name=None, carrying=None, passenger_seats_count=None, car_type='car'):
        super(Car, self).__init__(car_type, photo_file_name, brand, carrying)
        self.passenger_seats_count = passenger_seats_count

    def __str__(self):
        return ' '.join([self.car_type, self.photo_file_name, self.brand, self.carrying, self.passenger_seats_count])


class Truck(CarBase):
    def __init__(self, brand=None, photo_file_name=None, carrying=None, body_whl='0x0x0', car_type='truck'):
        super(Truck, self).__init__(car_type, photo_file_name, brand, carrying)
        try:
            self.body_length, self.body_width, self.body_height = self._initialize(body_whl)
        except:
            self.body_length, self.body_width, self.body_height = '0.0', '0.0', '0.0'

    def get_body_volume(self):
        return int(self.body_length) * int(self.body_width) * int(self.body_height)

    @staticmethod
    def _initialize(body_whl):
        return body_whl.split('x')

    def __str__(self):
        return ' '.join(
            [self.car_type, self.photo_file_name, self.brand, self.carrying, self.body_length, self.body_width,
             self.body_height])


class SpecMachine(CarBase):
    def __init__(self, brand=None, photo_file_name=None, carrying=None, extra=None, car_type='spec_machine'):
        super(SpecMachine, self).__init__(car_type, photo_file_name, brand, carrying)
        self.extra = extra

    def __str__(self):
        return ' '.join([self.car_type, self.photo_file_name, self.brand, self.carrying, self.extra])


class DoEverything:
    def __init__(self, path):
        self.path = path

    def do(self):
        car_list = self._read()
        car_data = self._validation(car_list)
        return car_data

    def _validation(self, car_list):
        car_data = []
        res = []
        for car in car_list:
            if (car != []) and self._isvalid(car):
                res = self._construct(car)
            car_data.append(res)
        return car_data

    @staticmethod
    def _construct(row):
        if row[0] == 'car':
            return Car(row[1], row[3], row[5], row[2])
        elif row[0] == 'truck':
            return Truck(row[1], row[3], row[5], row[4])
        else:
            return SpecMachine(row[1], row[3], row[5], row[6])

    @staticmethod
    def _isvalid(row):
        if row[0] == '':
            return False
        return True

    def _read(self):
        raw_data = []
        with open(self.path) as csv_fd:
            reader = csv.reader(csv_fd, delimiter=';')
            next(reader)
            for car in reader:
                raw_data.append(car)
        return raw_data


def get_car_list(path):
    result = DoEverything(path).do()
    return result


def main():
    result = get_car_list('cars.csv')
    print(result)


if __name__ == '__main__':
    main()
