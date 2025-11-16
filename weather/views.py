from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def weather_api(request, city):
    data = {
        "city": city,
        "temperature": 15,
        "unit": "celsius",
        "description": "Mostly cloudy",
        "api_source": "local_stub (Step 1)",
    }
    return JsonResponse(data)
