from datetime import datetime, timedelta
from django.utils import timezone
from api.models import WeatherReports, Countries, Cities
import random

COUNTRIES = [
    {'name': 'Россия', 'cities': ['Москва', 'Варкута']},
    {'name': 'Англия', 'cities': ['Лондон', 'Манчестер']},
    {'name': 'Германия', 'cities': ['Берлин', 'Гамбург']},
    {'name': 'США', 'cities': ['Нью-Йорк', 'Чикаго']}
]

VALUE_RANGE = {
    'pressure': [730, 790],
    'temperature': {'winter': [-40, 0], 'spring': [-10, 10], 'summer': [10, 40], 'autumn': [-10, 10]},
    'humidity': [20, 100],
    'wind_speed': [3, 10]
}

START_DATE = timezone.now() - timedelta(days=365)


def get_seasson(month_count):
    if month_count in [1, 2, 12]:
        return 'winter'
    if month_count in [3, 4, 5]:
        return 'spring'
    if month_count in [6, 7, 8]:
        return 'summer'
    if month_count in [9, 10, 11]:
        return 'autumn'
    return None


def create_weather_report(city):
    for i in range(366):
        curr_date = START_DATE + timedelta(days=i)
        season = get_seasson(curr_date.month)
        if season is None:
            raise ValueError('invalid season!')
        day_report = {}
        for j in range(24):
            temperature = 5 if j in list(range(20, 23)) + list(range(8)) else 0
            val = j % 2
            day_report[j] = WeatherReports.DEFAULT_VALUE
            day_report[j]['pressure'] = random.randint(VALUE_RANGE['pressure'][0], VALUE_RANGE['pressure'][1]) - val
            day_report[j]['humidity'] = random.randint(VALUE_RANGE['humidity'][0], VALUE_RANGE['humidity'][1]) - val
            day_report[j]['wind_speed'] = random.randint(VALUE_RANGE['wind_speed'][0], VALUE_RANGE['wind_speed'][1]) - val
            day_report[j]['temperature'] = random.randint(VALUE_RANGE['temperature'][season][0],
                                                          VALUE_RANGE['temperature'][season][1]) - temperature - val

        WeatherReports(city=city, date=curr_date, values=day_report).save()


def generate_data():
    for country in COUNTRIES:
        _ = Countries(name=country['name'])
        _.save()
        for city in country['cities']:
            c = Cities(name=city, country=_)
            c.save()
            create_weather_report(c)

# import init_db_data
# init_db_data.generate_data()
