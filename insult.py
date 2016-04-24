#!/usr/bin/python

from sopel.module import commands
import requests
import re

api = 'http://www.insultgenerator.org/'
nice_api = 'http://toykeeper.net/programs/mad/compliments'
nice_people = ('sharktamer', 'shane', 'donohoe', 'darkjesus', 'princess', 'declan')


@commands('insult')
def insult(bot, trigger):
    user = trigger.group(2)

    if any([n in user.lower() for n in nice_people]):
        r = requests.get(nice_api)
        #thread = re.search(r'(?:class="threadtitle"[^>]+>)([^<]+)', r.content)
        msg = re.search(r'(?<=class="blurb_title_1">)[^<]+', r.text).group(0)
        #msg = re.search('(?<=<br><br>)[^<]+', r.content).group(0)
        #print thread, post
    else:
        r = requests.get(api)
        msg = re.search(r'(?<=<br><br>)[^<]+', r.text).group(0)

    bot.say('{0}: {1}'.format(user, msg))

