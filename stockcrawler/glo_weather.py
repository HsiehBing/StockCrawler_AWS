import weathercom
import datetime
import json
import requests

def get_global_weather(msg):
    location = msg[1:]
    access_key = "66afe3e61b0f48759c3155534231302"
    today_get = (datetime.date.today() + datetime.timedelta(hours=10)).strftime("%Y-%m-%d %H")
    url = f'http://api.weatherapi.com/v1/forecast.json?key={access_key}&q={location}&dt={today_get}&aqi=yes'
    response = requests.get(url)
    
    data = json.loads(response.text)
    today= data['forecast']['forecastday'][0]['date']
    min_temp=data['forecast']['forecastday'][0]['day']['mintemp_c']
    max_temp=data['forecast']['forecastday'][0]['day']['maxtemp_c']
    c_o_rain= data['forecast']['forecastday'][0]['day'][ 'daily_chance_of_rain']
    feel_like = data['current']['feelslike_c']
    pm_2 = data['current']['air_quality']['pm2_5']

    return (f'  {today}\n    {location}\n體感溫度:{feel_like}度\n  pm2.5   :   {int(pm_2)}\n  最高溫   :{max_temp}度\n  最低溫   :{min_temp}度\n降雨機率 : {c_o_rain}%')





