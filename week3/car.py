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
        return self._extract_body_volume_from_string()

    def _extract_body_volume_from_string(self):
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


class FileSystemCarAdapter():
    pass


class CSVCarAdapter(FileSystemCarAdapter):
    def __init__(self, path):
        pass

    def get_cars(self, path):
        result = []
        raw_data = FileReader(path).read()
        for car_dict in raw_data:
            car_bool = CSVCarValidator(car_dict).validate()
            if car_bool:
                result.append(CSVCarConstructor(car_dict).construct())

        # self.data = self._get_data(path)
        # return Construct(self.data)

    # def _get_data(self, path):
    # return ReadFile.read(path)
class CSVCarConstructor:
    def __init__(self,car_dict):
        self.car_dict = car_dict
    def construct(self):
        if self.car_dict['car_type'] == 'car':
            return Car(self.car_dict['brand'], self.car_dict['photo_file_name'], self.car_dict['carrying'], self.car_dict['passenger_seats_count'])
        elif self.car_dict['car_type'] == 'truck':
            return Truck(self.car_dict['brand'], self.car_dict['photo_file_name'], self.car_dict['carrying'], self.car_dict['body_whl'])
        else:
            return SpecMachine(self.car_dict['brand'], self.car_dict['photo_file_name'], self.car_dict['carrying'], self.car_dict['extra'])

class CSVCarValidator:
    def __init__(self, car_dict):
        self.car_dict = car_dict

    def validate(self):
        pass

    def validate_file_ext(self):
        pass

    def validate_carrying(self):
        pass

    def validate_car_type(self):
        pass

    def validate_brand(self):
        pass

    def validate_seats_count(self):
        pass

'''
class Construct:
    def __init__(self, car_list):
        self.result_list = []
        for item in car_list:
            car = self.preconstruct(item)
            if car != None:
                self.result_list.append(car)

    def preconstruct(self, car):
        car = self._validation(car)
        if bool(car):
            return self._construct(car)

    @staticmethod
    def _validation(car_dict):
        if ((car_dict['car_type'] != '') and
                (car_dict['photo_file_name'] != 0) and
                (car_dict['brand'] != 0) and
                (car_dict['carrying'] != 0) and
                (os.path.splitext(car_dict['photo_file_name'])[1] in ['.jpg', '.jpeg', '.png', '.gif']) and (
                        (car_dict['passenger_seats_count'] != '') or (car_dict['extra'] != '') or (
                        car_dict['car_type'] == 'truck'))):
            try:
                float(car_dict['carrying'])
                return car_dict
            except:
                pass
        return {}

    @staticmethod
    def _construct(row):
        if row['car_type'] == 'car':
            return Car(row['brand'], row['photo_file_name'], row['carrying'], row['passenger_seats_count'])
        elif row['car_type'] == 'truck':
            return Truck(row['brand'], row['photo_file_name'], row['carrying'], row['body_whl'])
        else:
            return SpecMachine(row['brand'], row['photo_file_name'], row['carrying'], row['extra'])

'''
class FileReader:
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
    # raw_data = ReadFile('cars.csv').read()
    #result = CSVCarAdapter('cars.csv').smotryashii()
    # result = get_car_list('cars.csv')
    for car in result.result_list:
        print(car)


if __name__ == '__main__':
    main()
