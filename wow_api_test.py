import requests

token_file = open('wow_token.txt')
wow_token = token_file.readline()
character = 'Joyvimon'
realm = 'dunemaul'
parameters = {"fields": "items", "locale": "en_US", "apikey": wow_token}

response = requests.get("https://us.api.battle.net/wow/character/"+realm+'/'+character,params=parameters)
char = response.json()
character = response['name']
