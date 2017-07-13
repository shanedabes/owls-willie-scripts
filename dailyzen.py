#!/usr/bin/env python

from sopel.module import commands
import requests
import re
from html import unescape


@commands('zen')
def zen(bot, trigger):
    r = requests.get('https://www.dailyzen.com/')

    zr = re.search(r'<blockquote>\s*(?:<p>)?(.*?)(?:</p>)?\s*</blockquote>',
                   r.text.replace('\n', ' '))
    z = re.split(r'<br(?: /)?>', ' '.join(zr.group(1).split()))

    cr = re.search(r'<cite>(.*)</cite>', r.text.replace('\n', ' '))
    c = ' '.join(cr.group(1).split())

    for line in z:
        bot.say(unescape(line.strip()))
    bot.say(c.strip())
