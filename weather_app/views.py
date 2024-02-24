from django.shortcuts import render
from django.db import transaction
from asgiref.sync import sync_to_async
import httpx
import datetime

@sync_to_async
def fetch_city_data(city, api_key, current_weather_url):
    response = httpx.get(current_weather_url.format(city, api_key))
    return response.json()

@sync_to_async
def fetch_forecast_data(lat, lon, api_key, forecast_url):
    response = httpx.get(forecast_url.format(lat, lon, api_key))
    return response.json()

async def index(request):
    api_key = 'ab6e2f84bae424fb63597d5a13f2b3cc'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

    favorites = await sync_to_async(request.session.get)('favorites', [])
    history = await sync_to_async(request.session.get)('history', [])

    if request.method == 'POST':
        city = request.POST['city']
        history.append(city)
        request.session['history'] = history

        weather_data = await fetch_city_data(city, api_key, current_weather_url)
        lat, lon = weather_data['coord']['lat'], weather_data['coord']['lon']
        forecast_data = await fetch_forecast_data(lat, lon, api_key, forecast_url)

        context = {
            'weather_data': weather_data,
            'daily_forecasts': parse_forecast_data(forecast_data),
            'favorites': favorites,
            'history': history,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        context = {
            'favorites': favorites,
            'history': history,
        }
        return render(request, 'weather_app/index.html', context)

def parse_forecast_data(forecast_data):
    if not forecast_data:
        return []

    daily_forecasts = []
    for daily_data in forecast_data['daily'][:5]:
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
            'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
            'description': daily_data['weather'][0]['description'],
            'icon': daily_data['weather'][0]['icon'],
        })

    return daily_forecasts
