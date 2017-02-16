#!/usr/bin/env python

from sopel.module import commands
from sopel.formatting import color
import requests
import re
import random


@commands('checkiday')
def checkiday(bot, trigger):
    r = requests.get('https://www.checkiday.com/rss.php?tz=Europe/London')
    days = re.findall(r'<title>(.*?)</title>', r.text)[1:]
    colors = random.sample(range(2, 16), len(days))
    cdays = [color(i, j) + u'\x0f' for i, j in zip(days, colors)]
    out = 'Today is {}'.format(', '.join(cdays))
    bot.say(out)
