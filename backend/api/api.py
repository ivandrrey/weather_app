from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework import permissions, serializers, viewsets
from django.http import JsonResponse

from api.models import WeatherReports, Countries


# /api/get-data-form
class DataFormAPI(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def get(self, request):
        queryset = Countries.objects.prefetch_related('country_cities').all()
        countries_dict = {country.name: list(country.country_cities.values('id', 'name').all()) for country in queryset}
        return JsonResponse(countries_dict)


# /api/get-report-data
class WeatherReportsAPI(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def get(self, request):
        city_id = self.request.GET.get('city_id', None)
        if city_id is None:
            return JsonResponse({'errors': 'Miss city_id in request GET params'}, status=200)
        try:
            city_id = int(city_id)
        except ValueError:
            return JsonResponse({'errors': 'Invalid city_id in request GET params'}, status=200)
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)
        queryset = WeatherReports.objects
        if start_date is not None and end_date is not None:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return JsonResponse({'errors': 'Invalid format of date, need "YYYY.mm.dd"'}, status=200)
            if start_date == end_date:
                queryset = queryset.filter(date__year=start_date.year,
                                           date__month=start_date.month,
                                           date__day=start_date.day)
            else:
                queryset = queryset.filter(date__range=[start_date, end_date + timedelta(days=1)])
            queryset = queryset.filter(city_id=city_id).order_by('date').all()
            response = {r.date.strftime('%Y-%m-%d'): r.values for r in queryset}
            return JsonResponse(response)
        return JsonResponse({'errors': 'Miss date interval in request GET params'}, status=200)
