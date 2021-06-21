from django.db import models


# Create your models here.
class WeatherReports(models.Model):
    class Meta:
        db_table = 'weather_reports'
        verbose_name = 'Погодные сводки'

    DEFAULT_VALUE = {'pressure': 0, 'temperature': 0, 'humidity': 0, 'wind_speed': 0}

    city = models.ForeignKey('api.Cities', verbose_name=u'Страна', db_constraint=False, related_name='city_weather',
                             db_index=False, on_delete=models.CASCADE, to_field='id', blank=False, null=False)
    date = models.DateTimeField(verbose_name=u'Дата', blank=False, null=False)
    values = models.JSONField(verbose_name=u'Параметры по часам', default=dict)

    def save(self, *args, **kwargs):
        if self.values is None:
            self.values = self.get_default_values_dict()
        elif not self.is_valid_struct_of_values():
            raise ValueError("invalid structure of dict for field 'values' of model WeatherReports")

        super(WeatherReports, self).save(*args, **kwargs)

    def is_valid_struct_of_values(self):
        if isinstance(self.values, dict) and list(self.values.keys()) == list(range(0, 24)):
            try:
                is_valid = all(value.keys() == self.DEFAULT_VALUE.keys() and
                               all(isinstance(v, int) for v in value.values())
                               for value in self.values.values())
                return is_valid
            except AttributeError:
                pass
        return False

    def get_default_values_dict(self):
        return {i: self.DEFAULT_VALUE for i in range(0, 24)}


class Countries(models.Model):
    class Meta:
        db_table = 'countries'
        verbose_name = 'Страны'

    name = models.CharField(max_length=50, verbose_name=u'Название страны', blank=False, null=False)


class Cities(models.Model):
    class Meta:
        db_table = 'cities'
        verbose_name = 'Города'

    country = models.ForeignKey('api.Countries', verbose_name=u'Город', related_name='country_cities',
                                db_constraint=False, db_index=False, on_delete=models.CASCADE, to_field='id',
                                blank=False, null=False)
    name = models.CharField(max_length=50, verbose_name=u'Название города', blank=False, null=False)
