import requests

JOKE_URL = 'https://official-joke-api.appspot.com/random_joke'


def check_valid_status_code(request):  # to check if the status code from api is valid or not
    if request.status_code == 200: #It means if call is successfull
        return request.json() #return request in JSON format 
        
    return False #if unsuccessfull

def get_joke(): # to get a joke
    request = requests.get(JOKE_URL) #makes get request 
    data = check_valid_status_code(request) 

    return data
             
