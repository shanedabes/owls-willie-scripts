#!/usr/bin/python

from sopel.module import commands
import requests
import re
from random import choice

api = 'http://www.dickless.org/api/insult.xml'
nice_api = ('https://spreadsheets.google.com/feeds/list/'
            '1eEa2ra2yHBXVZ_ctH4J15tFSGEu-VTSunsrvaCAV598/'
            'od6/public/values?alt=json')
nice_people = ('sharktamer', 'shane', 'donohoe', 'darkjesus', 'princess',
               'declan')


@commands('insult')
def insult(bot, trigger):
    user = trigger.group(2)

    if any([n in user.lower() for n in nice_people]):
        r = requests.get(nice_api)
        compliments = [i['title']['$t'] for i in r.json()['feed']['entry']]
        msg = choice(compliments)
        # thread = re.search(r'(?:class="threadtitle"[^>]+>)([^<]+)', r.content)
        # msg = re.search(r'(?<=class="blurb_title_1">)[^<]+', r.text).group(0)
        # msg = re.search('(?<=<br><br>)[^<]+', r.content).group(0)
        # print thread, post
    else:
        r = requests.get(api)
        msg = re.search(r'<insult>(.*?)</insult>', r.text).groups()[0]

    bot.say('{0}: {1}'.format(user, msg))
