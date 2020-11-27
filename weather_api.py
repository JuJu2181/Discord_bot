import requests
import json

API_KEY = "40a9f65a9c29080b22a837ba05cbff0f"
def check_valid_status_code(request):  # to check if the status code from api is valid or not
    if request.status_code == 200: #It means if call is successfull
        return request.json() #return request in JSON format 
        
    return False #if unsuccessfull

def get_weather(city_name):
    WEATHER_URL = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}'
    request = requests.get(WEATHER_URL) #makes get request 
    data = check_valid_status_code(request) 
    return data

# weather_data = get_weather('Kathmandu')
# print(weather_data)
# print(type(weather_data))



    