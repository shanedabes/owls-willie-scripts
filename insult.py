#!/usr/bin/python

from sopel.module import commands
import requests
import re
from random import choice

api = 'https://insult.mattbas.org/api/insult.json'
nice_api = 'https://compliment-api.herokuapp.com/'
nice_people = ('sharktamer', 'shane', 'donohoe', 'darkjesus', 'princess',
               'declan')


@commands('insult')
def insult(bot, trigger):
    user = trigger.group(2)

    if any([n in user.lower() for n in nice_people]):
        r = requests.get(nice_api)
        #  compliments = [i['title']['$t'] for i in r.json()['feed']['entry']]
        #  msg = choice(compliments)
        msg = r.text
        # thread = re.search(r'(?:class="threadtitle"[^>]+>)([^<]+)', r.content)
        # msg = re.search(r'(?<=class="blurb_title_1">)[^<]+', r.text).group(0)
        # msg = re.search('(?<=<br><br>)[^<]+', r.content).group(0)
        # print thread, post
    else:
        r = requests.get(api)
        msg = r.json()['insult']

    bot.say('{0}: {1}'.format(user, msg))
