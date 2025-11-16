from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit

import urllib.request
import urllib.error
import json


# Create your views here.
@ratelimit(key="ip", rate="10/m", block=True)
def weather_api(request, city):
    # Cache
    cache_key = f"weather:{city.lower()}"
    cached_data = cache.get(cache_key)

    if cached_data:
        print(f"Data for {city} retrieved from cache")
        return JsonResponse(cached_data, json_dumps_params={"ensure_ascii": False})

    ## if not found in cache, get it from the API
    print(f"Data for {city} NOT found in cache. Fetching from API.")

    # API key
    api_key = settings.VISUAL_WEATHER_API_KEY

    if not api_key:
        return JsonResponse(
            {
                "error": "API key is missing. Set VISUAL_CROSSING_API_KEY in your .env file."
            },
            status=500,
        )

    # API url
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    unit_group = "metric"
    content_type = "json"

    # Construct the API request URL
    request_url = f"{base_url}{urllib.parse.quote(city)}?unitGroup={unit_group}&contentType={content_type}&key={api_key}"

    try:
        # Send the request to the Weather API
        with urllib.request.urlopen(request_url) as response:
            # Decode the JSON response
            response_data = response.read()
            weather_data = json.loads(response_data)

            # Print the resolved address and current weather information
            print(f"Weather Data for: {weather_data['resolvedAddress']}")
            print(f"Date: {weather_data['days'][0]['datetime']}")
            print("Temperature max:", weather_data["days"][0]["tempmax"])
            print("Temperature min:", weather_data["days"][0]["tempmin"])
            print("Conditions:", weather_data["days"][0]["description"])

            # Safety check to make sure the API response is valid
            if not weather_data.get("days") or len(weather_data["days"]) == 0:
                return JsonResponse(
                    {"error": "No forecast data found in API response."}, status=404
                )

            current_day = weather_data["days"][0]
            formatted_response = {
                "location": weather_data.get("resolvedAddress"),
                "date": current_day.get("datetime"),
                "temp_max": current_day.get("tempmax"),
                "temp_min": current_day.get("tempmin"),
                "conditions": current_day.get("description"),
                "source": "api_fresh",  # to see it's a fresh copy
            }

            cache.set(
                cache_key,
                formatted_response,
                timeout=12 * 60 * 60,  # save for 12 hours
            )

            return JsonResponse(
                formatted_response, json_dumps_params={"ensure_ascii": False}
            )

    except urllib.error.HTTPError as e:
        # This block is for errors from the API (e.g., 404, 401, 500)
        error_msg = f"Error fetching weather data: {e.code} {e.reason}"
        api_response = e.read().decode()

        print(f"Error fetching weather data: {e.code} {e.reason}")
        print("API response:", api_response)

        return JsonResponse(
            {"error": error_msg, "api_response": api_response}, status=e.code
        )

    except urllib.error.URLError as e:
        # This block is for connection errors (e.g., network down, DNS failed)
        error_msg = f"Error connecting to the API: {e.reason}"

        print(f"Error fetching weather data: {e.reason}")

        return JsonResponse(
            {"error": error_msg},
            status=503,  # 503 Service Unavailable
        )
