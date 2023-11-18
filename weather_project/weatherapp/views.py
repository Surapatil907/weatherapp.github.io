# views.py

from django.shortcuts import render, redirect
from .models import City
from .forms import Cityform
from django.http import HttpResponse
import requests

def get_weather_data(city):
    api_key = '2a6458de618ce1c2d067e3ec3fc3e731'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

def delete_city(request, city_id):
    try:
        city = City.objects.get(pk=city_id)
        city.delete()
    except City.DoesNotExist:
        pass  # City not found, do nothing

    return redirect('index')  # Redirect to the index view

def index(request):
    cities = City.objects.all()

    if request.method == 'POST':
        form = Cityform(request.POST)
        if form.is_valid():
            form.save()

    form = Cityform()
    weather_data = []

    for city in cities:
        city_weather = get_weather_data(city.name)
        if city_weather['cod'] == '404':
            continue
        weather = {
            'city': city.name,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'humidity': f"{city_weather['main']['humidity']} %",
            'pressure': f"{city_weather['main']['pressure']} hPa",
            'wind_speed': f"{city_weather['wind']['speed']} m/s",
            'id': city.id  # Pass the city ID for deletion
        }
        weather_data.append(weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'index.html', context)
