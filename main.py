from flask import Flask, request
# from geopy.geocoders import GoogleV3
import re
import requests

app = Flask(__name__)

MAPS_API_KEY = 'AIzaSyDepinwXk4HwdxyOwkwyBiBFqqTZytb_r8'
WEATHER_API_KEY = 'e4acb7ddf4d3c80a60d260259bd0d9c6'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}&units=metric'
# WEATHER_ICON_URL = 'https://openweathermap.org/img/wn/{}@4x.png'
WEATHER_ICON_URL = 'https://demo.whiteeye.id/static/weather_icons/{}@4x.png'
WEATHER_LOCATION_URL = 'http://api.openweathermap.org/geo/1.0/reverse?lat={}&lon={}&appid={}'
NOMINATIM_URL = 'https://nominatim.openstreetmap.org/reverse?lat={}&lon={}&format=json&accept-language=id'
plus_code_pattern = '(^|\s)([23456789CFGHJMPQRVWX]{4,6}\+[23456789CFGHJMPQRVWX]{2,3})(\s|$)'

HEADERS = {'user-agent': 'sltpn3-1.0.0'}


@app.route("/reverse_geocode")
def reverse_geocode():
    lat = request.args.get('lat', '')
    lon = request.args.get('lon', '')
    result = {'loc_name': ''}
    if lat and lon:
        url = NOMINATIM_URL.format(lat, lon)

        response = requests.get(url, headers=HEADERS)
        content = response.json()
        locs = []
        if 'road' in content['address']:
            locs.append(content['address']['road'])
        if 'village' in content['address']:
            locs.append(content['address']['village'])
        if 'city' in content['address']:
            locs.append(content['address']['city'])
        if 'county' in content['address']:
            locs.append(content['address']['county'])
        if 'state' in content['address']:
            locs.append(content['address']['state'])
        if 'country' in content['address']:
            locs.append(content['address']['country'])

        result['loc_name'] = ', '.join(locs[:3])
    return result


# @app.route("/weather")
# def weather():
#     coord = request.args.get('coord', '')
#     lat, lon = coord.replace(' ', '').split(',')
#     url = WEATHER_URL.format(lat, lon, WEATHER_API_KEY)
#     response = requests.get(url)
#     content = response.json()
#     weather_icon = WEATHER_ICON_URL.format(content['current']['weather'][0]['icon'])
#     temp_max = content['daily'][0]['temp']['max']
#     temp_min = content['daily'][0]['temp']['min']
#     temp_cur = content['current']['temp']
#     rain = content['daily'][0]['pop']*100
#     wind_speed = content['current']['wind_speed']*3.6
#     weather = content['current']['weather'][0]['description']
#     url = WEATHER_LOCATION_URL.format(lat, lon, WEATHER_API_KEY)
#     response = requests.get(url)
#     content = response.json()
#     location = content[0]['name']
#     result = {'icon': weather_icon,
#               'temp_max': temp_max,
#               'temp_min': temp_min,
#               'temp_cur': temp_cur,
#               'rain': rain,
#               'wind_speed': wind_speed,
#               'weather': weather,
#               'location': location}
#     return result
