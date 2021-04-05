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
        return ' '.join(
            [self.car_type, self.photo_file_name, self.brand, str(self.carrying), str(self.passenger_seats_count)])


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
            [self.car_type, self.photo_file_name, self.brand, str(self.carrying), self.body_length, self.body_width,
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
    @staticmethod
    def get_cars(path):
        result = []
        raw_data = FileReader(path).read()
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
        self._allowed_car_types = ['.jpg', '.jpeg', '.png', '.gif']

    def validate(self):
        if not self.validate_brand(self.car_dict['brand']):
            return False
        if not self.validate_file_ext(self.car_dict['photo_file_name']):
            return False
        if not self.validate_carrying(self.car_dict['carrying']):
            return False
        if not self.validate_car_type(self.car_dict['car_type']):
            return False
        if not self.validate_extra_property():
            return False
        return True

    def validate_file_ext(self, photo_file_name):
        if not os.path.splitext(photo_file_name)[1] in self._allowed_car_types:
            return False
        return True

    @staticmethod
    def validate_carrying(carrying):
        if carrying == '':
            return False
        try:
            float(carrying)
            return True
        except:
            return False

    @staticmethod
    def validate_car_type(car_type):
        if car_type == 'car' or car_type == 'truck' or car_type == 'spec_machine':
            return True
        return False

    @staticmethod
    def validate_brand(brand):
        if brand == '':
            return False
        return True

    def validate_extra_property(self):
        if self.car_dict['passenger_seats_count'] == '' and self.car_dict['car_type'] != 'truck' and \
                self.car_dict['extra'] == '':
            return False
        if self.car_dict['passenger_seats_count'] != '':
            try:
                int(self.car_dict['passenger_seats_count'])
                return True
            except:
                return False
        return True


class FileReader:
    def __init__(self, path):
        self.path = path

    def read(self):
        raw_data = []
        with open(self.path,errors="ignore") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                raw_data.append(row)
        return raw_data


def get_car_list(path):
    result = CSVCarAdapter().get_cars(path)
    return result


def main():
    result = get_car_list('cars.csv')
    for car in result:
        print(car)


if __name__ == '__main__':
    main()
