# -*- coding: utf-8 -*-
import csv
import os


class CarBase:
    def __init__(self, photo_file_name, brand, carrying):
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = carrying

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    car_type = 'car'

    def __init__(self, brand=None, photo_file_name=None, carrying=None, passenger_seats_count=None):
        super(Car, self).__init__(photo_file_name, brand, carrying)
        self.passenger_seats_count = passenger_seats_count

    def __str__(self):
        return ' '.join([self.car_type, self.photo_file_name, self.brand, self.carrying, self.passenger_seats_count])


class Truck(CarBase):
    car_type = 'truck'

    def __init__(self, brand=None, photo_file_name=None, carrying=None, body_whl='0.0x0.0x0.0'):
        super(Truck, self).__init__(photo_file_name, brand, carrying)
        try:
            self.body_length, self.body_width, self.body_height = self._initialize(body_whl)
        except:
            self.body_length, self.body_width, self.body_height = '0.0', '0.0', '0.0'

    def get_body_volume(self):
        return float(self.body_length) * float(self.body_width) * float(self.body_height)

    @staticmethod
    def _initialize(body_whl):
        return body_whl.split('x')

    def __str__(self):
        return ' '.join(
            [self.car_type, self.photo_file_name, self.brand, self.carrying, self.body_length, self.body_width,
             self.body_height])


class SpecMachine(CarBase):
    car_type = 'spec_machine'

    def __init__(self, brand=None, photo_file_name=None, carrying=None, extra=None):
        super(SpecMachine, self).__init__(photo_file_name, brand, carrying)
        self.extra = extra

    def __str__(self):
        return ' '.join([self.car_type, self.photo_file_name, self.brand, self.carrying, self.extra])


class Pasha:
    def __init__(self, path):
        self.path = path
        self.data = []

    def smotryashii(self):
        self.data = self._get_data(self.path)
        return Construct(self.data).preconstruct()

    def _get_data(self,path):
        return ReadFile.read(path)


class Construct:
    def __init__(self, car_list):
        self.car_list = car_list

    def preconstruct(self):
        car_data = []
        res = []
        for car in self.car_list:
            car = self._validation(car)
            if bool(car):
                res = self._construct(car)
                if res != None:
                    car_data.append(res)
        return car_data

    @staticmethod
    def _validation(car_dict):
        if ((car_dict['car_type'] != '') and
                (car_dict['photo_file_name'] != 0) and
                (car_dict['brand'] != 0) and
                (car_dict['carrying'] != 0) and
                (os.path.splitext(car_dict['photo_file_name'])[1] in ['.jpg', '.jpeg', '.png', '.gif'])):
            try:
                float(car_dict['carrying'])
                return car_dict
            except:
                pass
        return {}

    @staticmethod
    def _construct(row):
        if row['car_type'] == 'car' and row['passenger_seats_count'] != '':
            return Car(row['brand'], row['photo_file_name'], row['carrying'], row['passenger_seats_count'])
        elif row['car_type'] == 'truck':
            return Truck(row['brand'], row['photo_file_name'], row['carrying'], row['body_whl'])
        elif row['car_type'] == 'spec_machine' and row['extra'] != '':
            return SpecMachine(row['brand'], row['photo_file_name'], row['carrying'], row['extra'])
        else:
            return None


class ReadFile:
    def __init__(self, path):
        self.path = path

    def read(self):
        raw_data = []
        with open('cars.csv', errors="ignore") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                raw_data.append(row)
        return raw_data


'''
def get_car_list(path):
    result = DoEverything(path).do()
    return result
'''


def main():
    #raw_data = ReadFile('cars.csv').read()
    result = Pasha('cars.csv').smotryashii()
    # result = get_car_list('cars.csv')
    for car in result:
        print(car)


if __name__ == '__main__':
    main()
