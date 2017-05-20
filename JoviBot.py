import discord
import asyncio
import logging
import requests

#Discord API
token_file = open('token.txt')
token = token_file.readline()

client = discord.Client()

#Wow API
token_file = open('wow_token.txt')
wow_token = token_file.readline()

class_array = [None, 'Warrior', 'Paladin','Hunter','Rogue',
               'Priest', 'Death Knight', 'Shaman', 'Mage',
               'Warlock', 'Monk', 'Druid', 'Demon Hunter' ]

logging.basicConfig(level=logging.INFO)

@client.event
async def on_ready():
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('-----------')

    await client.change_presence(game=discord.Game(name='Pm Jovine w/ Issues'))


def get_wow_character(character, realm):
    parameters = {"fields": "items", "locale": "en_US", "apikey": wow_token}
    response = requests.get("https://us.api.battle.net/wow/character/" + realm + '/' + character, params=parameters)
    response = response.json()
    icon_url = 'http://render-api-us.worldofwarcraft.com/static-render/us/' + response['thumbnail']
    armory_url = 'https://worldofwarcraft.com/en-us/character/' + realm + '/' + character
    color = 0x0
    if response['faction'] == 0:
        color = 0x0000FF
    else:
        color = 0xFF0000
    em = discord.Embed(title=character + ' of ' + realm, colour=color, url=armory_url)
    em.set_thumbnail(url=icon_url)
    em.add_field(name='Item Level:', value=str(response['items']['averageItemLevel']))
    em.add_field(name='Class:', value=class_array[response['class']])
    return em

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    if message.content.startswith('^.^'):
        await client.send_message(message.channel,'^.^')
    elif message.content.startswith('^charlookup'):
        #expected format: ^charlookup  <realm> <name>
        info = message.content.split(' ')
        if len(info) != 3:
            await client.send_message(message.channel, 'Format: ^charlookup <realm> <name>')
            return
        realm = info[1]
        character = info[2]
        embed = get_wow_character(character, realm)
        await client.send_message(message.channel, embed=embed)


def main():
    client.run(token)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())