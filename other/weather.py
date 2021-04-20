import pprint
import sys

import requests
from dateutil.parser import parse


class WheatherForecast:
    def __init__(self):
        self._city_cache = {}

    def get(self, city):

        if city in self._city_cache:
            return self._city_cache[city]
        else:
            url = "https://community-open-weather-map.p.rapidapi.com/forecast"
            querystring = {"q": f"{city},rus"}

            headers = {
                'x-rapidapi-key': "f0ea62ce90msh3400c2d355763e9p10f15fjsncee3ea55a386",
                'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
            }

            data = requests.request("GET", url, headers=headers, params=querystring).json()
            forecast = [{'date': parse(data['list'][i]['dt_txt']),
                         'temp': int(data['list'][i]['main']['temp'] - 273)}
                        for i in range(5, 40, 8)]
            self._city_cache[city] = forecast
            return forecast


class CityInfo:
    def __init__(self, city, weaher_forecast=None):
        self.city = city
        self._weather_forecast = weaher_forecast or WheatherForecast()

    def weather_forecast(self):
        return self._weather_forecast.get(self.city)


def _main():
    city = sys.argv[1]
    city_info = CityInfo(city)
    forecast = city_info.weather_forecast()
    pprint.pprint(forecast)


if __name__ == '__main__':
    _main()
