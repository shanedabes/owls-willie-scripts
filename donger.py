#!/usr/bin/env python

from sopel.module import commands
import requests
import re
from random import choice


@commands('donger')
def donger(bot, trigger):
    url = 'http://dongerlist.com/'
    r = requests.get(url)
    pages = int(re.search(r'class="last".*?/([^/]*?)"', r.text).group(1))

    rpage = choice(range(1, pages+1))
    if rpage > 1:
        r = requests.get('http://dongerlist.com/page/{}'.format(rpage))
    dl = re.findall(r'data-clipboard-text="([^"]*)"', r.text)
    donger = choice(dl)

    bot.say(donger)
