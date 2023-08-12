"""Спроектировано из расчета что в файле присутствуют все колонки(содержание может быть пустым)"""
import csv
import os
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Type
import enum


class CarTypes(enum.Enum):
    car = "car"
    truck = "truck"
    spec_machine = "spec_machine"


@dataclass
class RawCar:
    car_type: str
    brand: str
    passenger_seats_count: str
    photo_file_name: str
    body_whl: str
    carrying: str
    extra: str


class BaseCarRepository(metaclass=ABCMeta):
    @abstractmethod
    def read_data(self) -> List[RawCar]:
        raise NotImplementedError


class BaseCarValidator(metaclass=ABCMeta):
    @abstractmethod
    def validate(self) -> bool:
        raise NotImplementedError


class BaseCarConstructor(metaclass=ABCMeta):
    @abstractmethod
    def construct(self):
        raise NotImplementedError


class CarBase:

    def __init__(self, photo_file_name: str, brand: str, carrying: str):
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = float(carrying)

    def get_photo_file_ext(self) -> str:
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    car_type = CarTypes.car

    def __init__(self, photo_file_name: str, brand: str, carrying: str, passenger_seats_count: str):
        super().__init__(photo_file_name, brand, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    car_type = CarTypes.truck

    def __init__(self, photo_file_name: str, brand: str, carrying: str, body_lwh: str):
        super().__init__(photo_file_name, brand, carrying)
        self.body_length, self.body_width, self.body_height = 0.0, 0.0, 0.0
        self._extract_lwh(body_lwh)

    def _extract_lwh(self, raw_string: str):
        lwh = raw_string.split("x")
        try:
            self.body_length, self.body_width, self.body_height = tuple(map(float, lwh))
        except ValueError:
            pass  # Тут можно нормальные ексепшины сделать

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    car_type = CarTypes.spec_machine

    def __init__(self, brand: str, photo_file_name: str, carrying: str, extra: str):
        super().__init__(photo_file_name, brand, carrying)
        self.extra = extra


class CSVCarRepository(BaseCarRepository):
    def __init__(self, path):
        self.path = path

    def read_data(self) -> List[RawCar]:
        raw_car_list = []
        with open(self.path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for car_dict in reader:
                raw_car_list.append(self._deserialize_car(car_dict))
        return raw_car_list

    @staticmethod
    def _deserialize_car(car_dict: Dict[str, str]) -> RawCar:
        return RawCar(car_dict["car_type"], car_dict["brand"], car_dict["passenger_seats_count"],
                      car_dict["photo_file_name"], car_dict["body_whl"], car_dict["carrying"], car_dict["extra"])


class CarValidator(BaseCarValidator):
    def __init__(self, raw_car: RawCar):
        self.raw_car = raw_car
        self._allowed_photo_types = ['.jpg', '.jpeg', '.png', '.gif']
        self._allowed_car_types = [car_type.value for car_type in CarTypes]

    def validate(self) -> bool:
        if not self._validate_brand():
            return False
        if not self._validate_file_ext():
            return False
        if not self._validate_carrying():
            return False
        if not self._validate_car_type():
            return False
        if not self._validate_extra_property():
            return False
        return True

    def _validate_brand(self) -> bool:
        return bool(self.raw_car.brand)

    def _validate_file_ext(self) -> bool:
        if os.path.splitext(self.raw_car.photo_file_name)[1] not in self._allowed_photo_types:
            return False
        return True

    def _validate_carrying(self) -> bool:
        if self.raw_car.carrying is None:
            return False
        try:
            float(self.raw_car.carrying)
            return True
        except ValueError:
            return False

    def _validate_car_type(self) -> bool:
        return self.raw_car.car_type in self._allowed_car_types

    def _validate_extra_property(self) -> bool:
        if self.raw_car.car_type == CarTypes.car.value:
            return self.raw_car.passenger_seats_count.isdigit()
        elif self.raw_car.car_type == CarTypes.spec_machine.value:
            return bool(self.raw_car.extra)
        else:
            return True


class CarConstructor(BaseCarConstructor):
    def __init__(self, raw_car):
        self.raw_car = raw_car

    def construct(self) -> CarBase:
        if self.raw_car.car_type == CarTypes.car.value:
            return Car(self.raw_car.photo_file_name, self.raw_car.brand, self.raw_car.carrying,
                       self.raw_car.passenger_seats_count)
        elif self.raw_car.car_type == CarTypes.truck.value:
            return Truck(self.raw_car.photo_file_name, self.raw_car.brand, self.raw_car.carrying, self.raw_car.body_whl)
        elif self.raw_car.car_type == CarTypes.spec_machine.value:
            return SpecMachine(self.raw_car.brand, self.raw_car.photo_file_name, self.raw_car.carrying,
                               self.raw_car.extra)


class CarOperator:  # Нейминг?
    def __init__(self, car_repository: BaseCarRepository,
                 CarValidator: Type[BaseCarValidator],
                 CarConstructor: Type[BaseCarConstructor]):
        # Каким кейсом в итоге называть то? # По умолчанию передать?
        self.car_repository = car_repository
        self.CarValidator = CarValidator
        self.CarConstructor = CarConstructor

    def get_cars(self) -> List[CarBase]:
        car_list = []
        raw_cars = self.car_repository.read_data()
        for raw_car in raw_cars:
            valid = self.CarValidator(raw_car).validate()
            # Как правильно интерфейс там сделать чтоб он ожидал аргумент?
            if valid:
                car_list.append(self.CarConstructor(raw_car).construct())
        return car_list


def get_car_list(path: str):
    operator = CarOperator(CSVCarRepository("cars.csv"), CarValidator, CarConstructor)
    return operator.get_cars()


if __name__ == '__main__':
    print(get_car_list("cars.csv"))
