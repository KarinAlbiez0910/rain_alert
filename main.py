import requests
import os
from twilio.rest import Client



api_key = os.environ.get('OWM_API_KEY')
phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
my_phone_number = os.environ.get("MY_PHONE_NUMBER")

parameters = {
    'lat': 48.13743,
    'lon': 11.57549,
    'appid': api_key,
    'exclude': "current,minutely,daily"
}

response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()

weather_data = response.json()


weather_ids = [item['weather'][0]['id'] for item in weather_data['hourly'][0:12]]

print(weather_ids)

res = any(item['weather'][0]['id'] < 700 for item in weather_data['hourly'][0:12])

if res:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="Bring an umbrella.",
        from_=phone_number,
        to=my_phone_number
    )

    print(message.status)
