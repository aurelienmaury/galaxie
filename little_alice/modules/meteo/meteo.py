#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org> all rights reserved
__author__ = 'Tuux'

import urllib
import json
import collections
import math
import getopt

"""Getopt Variables"""
version = '1.0'
verbose = False

"""Variables to configure"""
api_lang = 'fr'
api_url = 'http://api.openweathermap.org/data/2.5/'
api_q = 'guitrancourt,fr'
api_lat = '49.01'
api_lon = '1.78'
api_lang = 'fr'
api_mode = 'json'
api_id = '3012656'


def print_dump(data):
    print '--------------------------------------'
    """http://openweathermap.org/weather-data#current"""

    """City identification"""
    api_id = int(data['id'])
    print 'City identification  = ' + str(api_id)

    """Data receiving time, unix time, GMT"""
    api_dt = int(data['dt'])
    print 'Data receiving time, unix time, GMT  = ' + str(api_dt)

    """City name"""
    if 'name' in data:
        api_name = data['name']
        api_name.encode('utf-8')
        print 'City name  = ' + api_name

    """City geo location, lat"""
    api_coord_lat = float(data['coord_lat'])
    print 'City geo location, lat = ' + str(api_coord_lat)

    """City geo location, lon"""
    api_coord_lon = float(data['coord_lon'])
    print 'City geo location, lon = ' + str(api_coord_lon)

    """System parameter, do not use it"""
    api_sys_message = float(data['sys_message'])
    print 'System parameter, do not use it = ' + str(api_sys_message)

    """Country (GB, JP etc.)"""
    if 'sys_country' in data:
        api_sys_country = data['sys_country']
        api_sys_country.encode('utf-8')
        print 'City name  = ' + api_sys_country

    """Sunrise time, unix, UTC"""
    api_sys_sunrise = int(data['sys_sunrise'])
    print 'Sunrise time, unix, UTC = ' + str(api_sys_sunrise)

    """Sunset time, unix, UTC"""
    api_sys_sunset = int(data['sys_sunset'])
    print 'Sunset time, unix, UTC = ' + str(api_sys_sunset)

    """Temperature, Kelvin (subtract 273.15 to convert to Celsius) """
    if 'main_temp' in data:
        api_main_temp = float(data['main_temp'])
        print 'Temperature, Kelvin = ' + str(api_main_temp)

    """Humidity, % """
    api_main_humidity = int(data['main_humidity'])
    print 'Humidity, %  = ' + str(api_main_humidity)

    """Minimum temperature at the moment. 
    This is deviation from current temp that is possible for large cities 
    and megalopolises geographically expanded (use these parameter optionally)"""
    api_main_temp_min = float(data['main_temp_min'])
    print 'Minimum temperature, Kelvin = ' + str(api_main_temp_min)

    """Maximum temperature at the moment. 
    This is deviation from current temp that is possible for large cities 
    and megalopolises geographically expanded (use these parameter optionally)"""
    api_main_temp_max = float(data['main_temp_max'])
    print 'Maximum temperature, Kelvin = ' + str(api_main_temp_max)

    """Atmospheric pressure 
    (on the sea level, if there is no sea_level or grnd_level data), hPa"""
    if 'main_pressure' in data:
        api_main_pressure = int(data['main_pressure'])
        print 'Atmospheric pressure, hPa = ' + str(api_main_pressure)

    """Atmospheric pressure on the sea level, hP"""
    if 'main_sea_level' in data:
        api_main_sea_level = int(data['main_sea_level'])
        print 'Atmospheric pressure on the sea level, hPa = ' + str(api_sea_level)

    """Atmospheric pressure on the ground level, hPa"""
    if 'main_grnd_level' in data:
        api_main_grnd_level = int(data['main_grnd_level'])
        print 'Atmospheric pressure on the ground level, hPa  = ' + str(api_main_grnd_level)

    """Wind speed, mps"""
    if 'wind_speed' in data:
        api_wind_speed = float(data['wind_speed'])
        print 'Wind speed, mps   = ' + str(api_wind_speed)

    """Wind direction, degrees (meteorological) """
    if 'wind_deg' in data:
        api_wind_deg = int(data['wind_deg'])
        print 'Wind direction, degrees (meteorological) = ' + str(api_wind_deg)

    """Wind gust, mps"""
    if 'wind_gust' in data:
        api_wind_gust = float(data['wind_gust'])
        print 'Wind gust, mps = ' + str(api_wind_gust)

    """Wind gust, mps"""
    if 'wind_gust' in data:
        api_wind_gust = float(data['wind_gust'])
        print 'Wind gust, mps = ' + str(api_wind_gust)

    """Cloudiness, %"""
    if 'clouds_all' in data:
        api_clouds_all = float(data['clouds_all'])
        print 'Cloudiness, % = ' + str(api_clouds_all)

    """weather (more info Weather condition codes):"""
    """http://openweathermap.org/weather-conditions"""
    """Weather condition id"""
    if 'weather_0_id' in data:
        api_weather_0_id = int(data['weather_0_id'])
        print 'Weather condition id  = ' + str(api_weather_0_id)

    if 'weather_0_main' in data:
        api_weather_0_main = data['weather_0_main']
        api_weather_0_main.encode('utf-8')
        print 'Group of weather parameters (Rain, Snow, Extreme etc.)   = ' + api_weather_0_main

    if 'weather_0_description' in data:
        api_weather_0_description = data['weather_0_description']
        api_weather_0_description.encode('utf-8')
        print 'Weather Description  = ' + api_weather_0_description

    if 'weather_0_icon' in data:
        api_weather_0_icon = data['weather_0_icon']
        api_weather_0_icon.encode('utf-8')
        print 'Weather icon id  = ' + api_weather_0_icon

    if 'weather_1_id' in data:
        api_weather_1_id = int(data['weather_1_id'])
        print 'Weather condition id  = ' + str(api_weather_1_id)

    if 'weather_1_main' in data:
        api_weather_1_main = data['weather_1_main']
        api_weather_1_main.encode('utf-8')
        print 'Group of weather parameters (Rain, Snow, Extreme etc.)   = ' + api_weather_1_main

    if 'weather_1_description' in data:
        api_weather_1_description = data['weather_1_description']
        api_weather_1_description.encode('utf-8')
        print 'Weather Description  = ' + api_weather_1_description

    if 'weather_1_icon' in data:
        api_weather_1_icon = data['weather_1_icon']
        api_weather_1_icon.encode('utf-8')
        print 'Weather icon id  = ' + api_weather_1_icon


def print_human_dump(data):
    """City name"""
    if 'name' in data:
        api_name = data['name']
        #api_name.encode('utf-8')
        print api_name + ',',

    # """Country (GB, JP etc.)"""
    # if 'sys_country' in data:
    #     api_sys_country = data['sys_country']
    #     #api_sys_country.encode('utf-8')
    #     print api_sys_country

    """Temperature, Kelvin (subtract 273.15 to convert to Celsius) """
    if 'main_temp' in data:
        api_main_temp = float(data['main_temp'])
        api_main_temp = convert_f2c(api_main_temp)
        api_main_temp = api_main_temp.replace('.',',')
        print str(api_main_temp) + '° Celcius, ',

    if 'weather_0_description' in data:
        api_weather_0_description = data['weather_0_description']
        #api_weather_0_description.encode('utf-8')
        print api_weather_0_description + ' '


def get_current_weather_data_by_city_name():
    options = 'weather?q=%s&lang=%s&mode=%s' % (api_q, api_lang, api_mode)
    url = api_url + options
    request = urllib.urlopen(url)
    data = request.read()
    data = json.loads(data)
    # DEBUG Infos   
    # print(json.dumps(flatten_dict(data), indent=4, sort_keys=True))
    data = flatten_dict(data)
    print_human_dump(data)
    return data


def give_temperature(data):
    api_main_temp = float(data['main_temp'])
    api_main_temp = convert_f2c(api_main_temp)
    print str(api_main_temp) + '°'


def flatten_dict(d, parent_key=''):
    """Recursively flatten a dict"""
    items = []
    for k, v in d.items():
        new_key = parent_key + '_' + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v, new_key).items())
        elif type(v) == list:
            for n in range(len(v)):
                mykey = "%s_%d" % (new_key, n)
                items.extend(flatten_dict(v[n], mykey).items())
        else:
            items.append((new_key, v))
    return dict(items)


def convert_f2c(S):
    fahrenheit = float(S)
    celsius = "%.1f" % (fahrenheit - 273.15)
    return celsius


def to_weather_condition_description(weather_id):
    if weather_id == 200:
        return str("thunderstorm with light rain")
    elif weather_id == 804:
        return str("overcast clouds ")
    else:
        return str(weather_id)


def to_wind_description(speed):
    if 0.000 <= speed <= 0.299:
        return str("Calme")
    elif 0.300 <= speed <= 1.599:
        return str("Très légère brise")
    elif 1.600 <= speed <= 3.399:
        return str("Légère brise")
    elif 3.400 <= speed <= 5.499:
        return str("Petite brise")
    elif 5.500 <= speed <= 7.999:
        return str("Jolie brise")
    elif 8.000 <= speed <= 10.799:
        return str("Bonne brise")
    elif 10.800 <= speed <= 13.899:
        return str("Vent frais")
    elif 13.900 <= speed <= 17.199:
        return str("Grand frais")
    elif 17.200 <= speed <= 20.799:
        return str("Coup de vent")
    elif 20.800 <= speed <= 24.499:
        return str("Fort coup de vent")
    elif 24.500 <= speed <= 28.499:
        return str("Tempête")
    elif 28.500 <= speed <= 32.699:
        return str("Violente tempête")
    elif speed >= 32.700:
        return str("Ouragan")


if __name__ == "__main__":
    get_current_weather_data_by_city_name()
