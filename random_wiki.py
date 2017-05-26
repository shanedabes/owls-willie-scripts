#!/usr/bin/env python

import requests
import re
from sopel.module import commands

@commands('rw')
def random_wiki(bot, trigger):
    r = requests.get('https://en.wikipedia.org/wiki/Special:Random')

    title = re.search(r'<title>(.*) - .*?</title>', r.text).group(1)

    bot.say('{}: {}'.format(title, r.url))
