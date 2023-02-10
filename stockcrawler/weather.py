#W
import requests
import json
def get_weather(msg):
    locationName = msg[1:]
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": "CWB-43E69F60-8DCC-400E-95A4-F59768D86469",
        "locationName": locationName,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = json.loads(response.text)
        location = data["records"]["location"][0]["locationName"]
        weather_elements = data["records"]["location"][0]["weatherElement"]
        start_time = weather_elements[0]["time"][0]["startTime"][10:13]
        end_time = weather_elements[0]["time"][0]["endTime"][10:13]
        weather_state = weather_elements[0]["time"][0]["parameter"]["parameterName"]
        rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
        max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]
        final_part =(f'{location}{start_time}-{end_time}  {weather_state} 降雨機率{rain_prob}% 最低溫 {min_tem}度 最高溫{max_tem}度')
        return final_part


