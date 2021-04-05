# -*- coding: utf-8 -*-
import csv
import os
from abc import abstractmethod, ABCMeta


class CarBase:
    def __init__(self, photo_file_name, brand, carrying):
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = carrying

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super(Car, self).__init__(photo_file_name, brand, carrying)
        self.passenger_seats_count = passenger_seats_count

    def __str__(self):
        return ' '.join(
            [self.car_type, self.photo_file_name, self.brand, str(self.carrying), str(self.passenger_seats_count)])


class Truck(CarBase):
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super(Truck, self).__init__(photo_file_name, brand, carrying)
        self.body_whl = body_whl
        self.body_length = 0.0
        self.body_width = 0.0
        self.body_height = 0.0
        self._extract_body_volume_from_string()

    def get_body_volume(self):
        return self.body_width * self.body_length * self.body_height

    def _extract_body_volume_from_string(self):
        try:
            self.body_length, self.body_width, self.body_height = self.body_whl.split('x')
        except:
            pass

    def __str__(self):
        return ' '.join(
            [self.car_type, self.photo_file_name, self.brand, str(self.carrying), str(self.body_length),
             str(self.body_width),
             str(self.body_height)])


class SpecMachine(CarBase):
    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        super(SpecMachine, self).__init__(photo_file_name, brand, carrying)
        self.extra = extra

    def __str__(self):
        return ' '.join([self.car_type, self.photo_file_name, self.brand, str(self.carrying), self.extra])


class FileSystemCarAdapter(metaclass=ABCMeta):
    @abstractmethod
    def get_cars(self, path):
        raise NotImplementedError


class CSVCarAdapter(FileSystemCarAdapter):
    def __init__(self, filename):
        self.filename = filename

    def get_cars(self, path):
        result = []
        final_path = path + '/' + self.filename
        raw_data = FileReader(final_path).read()
        for car_dict in raw_data:
            car_bool = CSVCarValidator(car_dict).validate()
            if car_bool:
                result.append(CSVCarConstructor(car_dict).construct())
        return result


class CSVCarConstructor:
    def __init__(self, car_dict):
        self.car_dict = car_dict

    def construct(self):
        if self.car_dict['car_type'] == 'car':
            return Car(self.car_dict['brand'], self.car_dict['photo_file_name'], float(self.car_dict['carrying']),
                       int(self.car_dict['passenger_seats_count']))
        elif self.car_dict['car_type'] == 'truck':
            return Truck(self.car_dict['brand'], self.car_dict['photo_file_name'], float(self.car_dict['carrying']),
                         self.car_dict['body_whl'])
        else:
            return SpecMachine(self.car_dict['brand'], self.car_dict['photo_file_name'],
                               float(self.car_dict['carrying']),
                               self.car_dict['extra'])


class CSVCarValidator:
    def __init__(self, car_dict):
        self.car_dict = car_dict
        self._allowed_photo_types = ['.jpg', '.jpeg', '.png', '.gif']
        self._allowed_car_types = ['car', 'truck', 'spec_machine']

    def validate(self):
        if not self.validate_brand():
            return False
        if not self.validate_file_ext():
            return False
        if not self.validate_carrying():
            return False
        if not self.validate_car_type():
            return False
        if not self.validate_extra_property():
            return False
        return True

    def validate_file_ext(self):
        if not os.path.splitext(self.car_dict['photo_file_name'])[1] in self._allowed_photo_types:
            return False
        return True

    def validate_carrying(self):
        if self.car_dict['carrying'] == '':
            return False
        try:
            float(self.car_dict['carrying'])
            return True
        except:
            return False

    def validate_car_type(self):
        return self.car_dict['car_type'] in self._allowed_car_types

    def validate_brand(self):
        return bool(self.car_dict['brand'])

    def validate_extra_property(self):
        if self.car_dict['car_type'] == 'car':
            return self.car_dict['passenger_seats_count'].isdigit()
        elif self.car_dict['car_type'] == 'spec_machine':
            return bool(self.car_dict['extra'])
        else:
            return True


class FileReader:
    def __init__(self, path):
        self.path = path

    def read(self):
        raw_data = []
        with open(self.path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                raw_data.append(row)
        return raw_data


def get_car_list(filename):
    result = CSVCarAdapter(filename).get_cars(os.getcwd())
    return result


def main():
    result = get_car_list('cars.csv')
    for car in result:
        print(car)


if __name__ == '__main__':
    main()
