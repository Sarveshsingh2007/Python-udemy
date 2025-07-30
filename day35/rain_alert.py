import requests
from twilio.rest import Client

Open_Weather_Map_Endpoint = "http://api.openweathermap.org/data/2.5/forecast?"
# api_key = "d837f08f65527d2c882b33b4e4f8b793"
# account_sid = 
# auth_token = 


weather_parameters = {
    "lat": 29.403299,
    "lon": 80.087898,
    "appid": api_key,
    "cnt": 4
}

response = requests.get(Open_Weather_Map_Endpoint, params=weather_parameters)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for hour_data in weather_data['list']:
    condition_code = hour_data['weather'][0]['id']
    if int(condition_code) < 700:
        will_rain = True    
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="Light to Moderate Rain accompanied with thunderstorm/gusty wind (50-60 kmph)/intense spell of rain is very likely to occur at most places over Almora, Champawat, Haridwar, Nainital, Pauri Garhwal, Udham Singh Nagar in next 3 hours.",
        from_="+14027355079",
        to= "+9163953379",
    )
    print(message.status)    
