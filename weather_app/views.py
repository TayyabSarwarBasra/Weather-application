# from django.shortcuts import render
# import requests
# import datetime
#
# def index(request):
#     api_key = 'ab6e2f84bae424fb63597d5a13f2b3cc'
#     current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
#     # current_weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=YOUR_API_KEY&units=metric'
#     # forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'
#     forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'
#     forecast_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
#
#     if request.method == 'POST':
#         city1 = request.POST['city1']
#         city2 = request.POST.get('city2', None)
#
#         weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)
#
#         if city2:
#             weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url,
#                                                                          forecast_url)
#         else:
#             weather_data2, daily_forecasts2 = None, None
#
#         context = {
#             'weather_data1': weather_data1,
#             'daily_forecasts1': daily_forecasts1,
#             'weather_data2': weather_data2,
#             'daily_forecasts2': daily_forecasts2,
#         }
#
#         return render(request, 'weather_app/index.html', context)
#     else:
#         return render(request, 'weather_app/index.html')
#
#
# def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
#     response = requests.get(current_weather_url.format(city, api_key)).json()
#     lat, lon = response['coord']['lat'], response['coord']['lon']
#
#
#     forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
#
#     if forecast_response['cod'] != 200:
#         print(f"Error in forecast API request. Status code: {forecast_response['cod']}")
#         return None, []
#
#     weather_data = {
#         'city': city,
#         'temperature': round(response['main']['temp'] - 273.15, 2),
#         'description': response['weather'][0]['description'],
#         'icon': response['weather'][0]['icon'],
#     }
#
#     daily_forecasts = []
#     for daily_data in forecast_response['daily'][:5]:
#         daily_forecasts.append({
#             'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
#             'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
#             'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
#             'description': daily_data['weather'][0]['description'],
#             'icon': daily_data['weather'][0]['icon'],
#         })
#
#     return weather_data, daily_forecasts

#
# from django.shortcuts import render
# import httpx
# import datetime
#
#
# async def index(request):
#     api_key = 'ab6e2f84bae424fb63597d5a13f2b3cc'
#     current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
#     forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'
#
#     favorites = request.session.get('favorites', [])
#     history = request.session.get('history', [])
#
#     if request.method == 'POST':
#         city1 = request.POST['city1']
#         weather_data1, daily_forecasts1 = await fetch_weather_and_forecast(city1, api_key, current_weather_url,
#                                                                            forecast_url)
#
#         context = {
#             'weather_data1': weather_data1,
#             'daily_forecasts1': daily_forecasts1,
#             'favorites': favorites,
#             'history': history,
#         }
#
#         return render(request, 'weather_app/index.html', context)
#     else:
#         context = {
#             'favorites': favorites,
#             'history': history,
#         }
#         return render(request, 'weather_app/index.html', context)
#
#
# async def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
#     async with httpx.AsyncClient() as client:
#         current_response = await client.get(current_weather_url.format(city, api_key))
#         current_data = current_response.json()
#
#         if current_response.status_code != 200:
#             print(f"Error in current weather API request. Status code: {current_response.status_code}")
#             return None, []
#
#         lat, lon = current_data['coord']['lat'], current_data['coord']['lon']
#
#         forecast_response = await client.get(forecast_url.format(lat, lon, api_key))
#         forecast_data = forecast_response.json()
#
#         if forecast_response.status_code != 200:
#             print(f"Error in forecast API request. Status code: {forecast_response.status_code}")
#             return None, []
#
#     weather_data = {
#         'city': city,
#         'temperature': round(current_data['main']['temp'] - 273.15, 2),
#         'description': current_data['weather'][0]['description'],
#         'icon': current_data['weather'][0]['icon'],
#     }
#
#     daily_forecasts = []
#     for daily_data in forecast_data['daily'][:5]:
#         daily_forecasts.append({
#             'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
#             'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
#             'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
#             'description': daily_data['weather'][0]['description'],
#             'icon': daily_data['weather'][0]['icon'],
#         })
#
#     return weather_data, daily_forecasts
#
#
# from django.shortcuts import render
# from django.db import transaction
# from asgiref.sync import sync_to_async
# import httpx
# import datetime
#
# @sync_to_async
# def fetch_city_data(city, api_key, current_weather_url):
#     response = httpx.get(current_weather_url.format(city, api_key))
#     return response.json()
#
# @sync_to_async
# def fetch_forecast_data(lat, lon, api_key, forecast_url):
#     response = httpx.get(forecast_url.format(lat, lon, api_key))
#     return response.json()
#
# async def index(request):
#     api_key = 'ab6e2f84bae424fb63597d5a13f2b3cc'
#     current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
#     forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'
#
#     favorites = await sync_to_async(request.session.get)('favorites', [])
#     history = await sync_to_async(request.session.get)('history', [])
#
#     if request.method == 'POST':
#         city = request.POST['city1']
#         history.append(city)
#         request.session['history'] = history
#
#         weather_data = await fetch_city_data(city, api_key, current_weather_url)
#         lat, lon = weather_data['coord']['lat'], weather_data['coord']['lon']
#         forecast_data = await fetch_forecast_data(lat, lon, api_key, forecast_url)
#
#         context = {
#             'weather_data': weather_data,
#             'daily_forecasts': parse_forecast_data(forecast_data),
#         }
#
#         if request.is_ajax():
#             return render(request, 'weather_app/weather_data.html', context)
#         else:
#             return render(request, 'weather_app/index.html', context)
#     else:
#         context = {
#             'favorites': favorites,
#             'history': history,
#         }
#         return render(request, 'weather_app/index.html', context)
#
# def parse_forecast_data(forecast_data):
#     if not forecast_data:
#         return []
#
#     daily_forecasts = []
#     for daily_data in forecast_data['daily'][:5]:
#         daily_forecasts.append({
#             'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
#             'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
#             'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
#             'description': daily_data['weather'][0]['description'],
#             'icon': daily_data['weather'][0]['icon'],
#         })
#
#     return daily_forecasts
#
# from django.shortcuts import render
# import httpx
# import datetime
#
# async def fetch_city_data(city, api_key, current_weather_url):
#     response = await httpx.get(current_weather_url.format(city, api_key))
#     return response.json()
#
# async def fetch_forecast_data(lat, lon, api_key, forecast_url):
#     response = await httpx.get(forecast_url.format(lat, lon, api_key))
#     return response.json()
#
# async def index(request):
#     api_key = 'ab6e2f84bae424fb63597d5a13f2b3cc'
#     current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
#     forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'
#
#     favorites = request.session.get('favorites', [])
#     history = request.session.get('history', [])
#
#     if request.method == 'POST':
#         city = request.POST['city']
#         history.append(city)
#         request.session['history'] = history
#
#         weather_data = await fetch_city_data(city, api_key, current_weather_url)
#         lat, lon = weather_data['coord']['lat'], weather_data['coord']['lon']
#         forecast_data = await fetch_forecast_data(lat, lon, api_key, forecast_url)
#
#         context = {
#             'weather_data': weather_data,
#             'daily_forecasts': parse_forecast_data(forecast_data),
#             'favorites': favorites,
#             'history': history,
#         }
#
#         return render(request, 'weather_app/index.html', context)
#     else:
#         context = {
#             'favorites': favorites,
#             'history': history,
#         }
#         return render(request, 'weather_app/index.html', context)
#
# def parse_forecast_data(forecast_data):
#     if not forecast_data:
#         return []
#
#     daily_forecasts = []
#     for daily_data in forecast_data['daily'][:5]:
#         daily_forecasts.append({
#             'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
#             'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
#             'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
#             'description': daily_data['weather'][0]['description'],
#             'icon': daily_data['weather'][0]['icon'],
#         })
#
#     return daily_forecasts


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
