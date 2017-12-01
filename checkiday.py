#!/usr/bin/env python

from sopel.module import commands
from sopel.formatting import color
import requests
import re
import random
from itertools import cycle


@commands('days')
def checkiday(bot, trigger):
    r = requests.get('https://www.checkiday.com/rss.php?tz=Europe/London')
    days = re.findall(r'<title>(.*?)</title>', r.text)[1:]

    colors = cycle(random.sample([2, 3, 4, 6, 7, 14, 15], 7))
    cdays = [color(i, j) + u'\x0f' for i, j in zip(days, colors)]
    out = 'Today is {}'.format(', '.join(cdays))
    bot.say(out, max_messages=10)
