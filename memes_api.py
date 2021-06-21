import requests
import random
import pycurl


#MEME_URL = 'https://api.ksoft.si/images/random-meme'
MEME_URL = 'https://www.memedroid.com/memes/random'
headers1 = {
    'Authorization': 'eyJ0IjogImFwcCIsICJrIjogImtobWFjc2lnIiwgInBrIjogbnVsbCwgIm8iOiAiNjI0OTQ3MzgyNDIxMDI4ODY4IiwgImMiOiAxMDM4NDIyN30.e005908cf61d864135a18b8defaeb9fa9184a67076e941f871756b56de00de07',
}

def check_valid_status_code(request):  # to check if the status code from api is valid or not
    if request.status_code == 200: #It means if call is successfull
        return request.json() #return request in JSON format 
        
    return False #if unsuccessfull

def random_meme(): # to get a joke
    request = requests.get(MEME_URL) #makes get request 
    data = check_valid_status_code(request) 
    return data



meme_data = random_meme()
print(meme_data)
