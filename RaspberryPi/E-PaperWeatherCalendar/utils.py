# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 20:23:01 2021

@author: Fred Hu
"""

#import libraries
import datetime
import json
from requests import get
import logging

#index of X for month
monthDict = {'January': 210,
            'February':205,
            'March':230,
            'April':240,
            'May':250,
            'June':245,
            'July':250,
            'August':225,
            'September':200,
            'October':225,
            'November':205,
            'December':200,}

#API Key
#Replace with your own heWeatherKey
heWeatherKey = "*************************"

#return the index of X for month
def getMonthX(monthStr):
    return monthDict[monthStr]

#return current time
def getCurrentTime():
    currentTime = datetime.datetime.now() 
    date = currentTime.date()
    dateStr = date.strftime('%Y/%m/%d')
    weekStr = date.strftime('%A')
    dayStr = date.strftime('%d')
    monthStr = date.strftime('%B')
    return dateStr, weekStr, dayStr, monthStr

#get the locationID and city name for current city
def getLocationID():
    try:
        response = get('https://api.myip.la/en?json	json')
        locationInfo = json.loads(response.text)['location']
        province = locationInfo['province']
        city = locationInfo['city']
    except Exception as e:
        logging.info(e)
        province = 'Jiangsu'
        city = 'Yangzhou'
    
    try:
        response = get("https://geoapi.qweather.com/v2/city/lookup?adm=" 
                       + province + "&location=" + city + "&key="
                       + heWeatherKey)
        locationInfo = json.loads(response.text)['location']
        locationID = locationInfo[0]['id']
        city = locationInfo[0]['name']
    except Exception as e:
        logging.info(e)
        locationID = "101190601"
        city = "扬州"
    return locationID, city

#get the information of weather
def getWeather():
    locationID, city = getLocationID()
    try:
        response = get("https://devapi.qweather.com/v7/weather/now?" +
                       "location=" + locationID + "&key=" + heWeatherKey)
        nowWeather = json.loads(response.text)['now']
        temp = nowWeather['temp']
        icon = nowWeather['icon']
        text = nowWeather['text']
    except Exception as e:
        temp = 'N/A'
        icon = '999'
        text = "未知"
    
    try:
        response = get("https://devapi.qweather.com/v7/weather/3d?" +
                       "location=" + locationID + "&key=" + heWeatherKey)
        dailyWeather = json.loads(response.text)['daily'][0]
        tempMin = dailyWeather['tempMin']
        tempMax = dailyWeather['tempMax']
    except Exception as e:
        logging.info(e)
        tempMin = "N/A"
        tempMax = "N/A"
    return city, temp, icon, text, tempMin, tempMax