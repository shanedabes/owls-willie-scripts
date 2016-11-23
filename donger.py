#!/usr/bin/env python

from sopel.module import commands
import requests
import re
from random import choice


@commands('donger')
def donger(bot, trigger):
    args = trigger.group(2)
    if args:
        cat = args.split()[0].lower()
        cat_url = 'http://dongerlist.com/category/{}'.format(cat)
        r = requests.get(cat_url)
        if r.status_code == 200:
            url = cat_url
        else:
            bot.say('No {} category'.format(cat))
            bot.say('Find categories at dongerlist.com')
            return
    else:
        url = 'http://dongerlist.com/'

    r = requests.get(url)
    pages_re = re.findall(r'class="last".*?/([^/]*?)"', r.text)
    if not pages_re:
        pages_re = re.findall(r'class=".*?larger".*?>(\d+)<', r.text)

    if pages_re:
        pages = int(pages_re[-1])
    else:
        pages = 1

    rpage = choice(range(1, pages+1))
    if rpage > 1:
        r = requests.get('http://dongerlist.com/page/{}'.format(rpage))
    dl = re.findall(r'data-clipboard-text="([^"]*)"', r.text)
    donger = choice(dl)

    bot.say(donger)
