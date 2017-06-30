#!/usr/bin/env python

from sopel.module import commands
import requests
import re

@commands('zen')
def zen(bot, trigger):
    r = requests.get('https://www.dailyzen.com/')

    zr = re.search(r'<blockquote>(.*)</blockquote>', r.text.replace('\n', ' '))
    z = ' '.join(zr.group(1).split()).split('<BR>')

    cr = re.search(r'<cite>(.*)</cite>', r.text.replace('\n', ' '))
    c = ' '.join(cr.group(1).split())

    for line in z:
        bot.say(line)
    bot.say(c)
