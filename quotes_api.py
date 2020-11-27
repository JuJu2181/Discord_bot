import requests
import random

QUOTE_URL = 'https://type.fit/api/quotes'


def check_valid_status_code(request):  # to check if the status code from api is valid or not
    if request.status_code == 200: #It means if call is successfull
        return request.json() #return request in JSON format 
        
    return False #if unsuccessfull

def get_quote(): # to get a joke
    request = requests.get(QUOTE_URL) #makes get request 
    data = check_valid_status_code(request) 
    return data[random.randint(1,1640)]

# quote = get_quote()
# # print(quote[random.randint(1, 1640)])
# print(quote['text'] + '\n - ' + quote['author'])