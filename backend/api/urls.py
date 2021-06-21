from django.urls import path

from .api import (
    DataFormAPI,
    WeatherReportsAPI,
)


# /api/
urlpatterns = [
    path('get-data-form/', DataFormAPI.as_view()),
    path('get-report-data/', WeatherReportsAPI.as_view()),
]