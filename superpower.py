#!/usr/bin/env python

import requests
import re
from sopel.module import commands


@commands('superpower')
def superpower(bot, trigger):
    r = requests.get('http://powerlisting.wikia.com/wiki/Special:Random')
    name = re.search('<h1.*>.*?</h1>', r.text).group()
    desc = re.search('<p>.*', r.text).group()

    name, desc = [re.sub(r'<.*?>', '', i) for i in (name, desc)]
    out = '{}: {} ({})'.format(name, desc, r.url)

    bot.say(out)
