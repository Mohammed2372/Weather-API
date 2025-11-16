from django.urls import path

from .views import weather_api

urlpatterns = [
    path("<str:city>/", weather_api, name="weather"),
]
