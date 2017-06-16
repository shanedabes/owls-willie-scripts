#!/usr/bin/env python

from sopel.module import commands
# import requests


@commands('meme')
def meme(bot, trigger):
    if not trigger.group(2) or trigger.group(2).count('/') < 2:
        bot.say('Usage: .meme meme_type/top_text/bottom_text')
        return

    meme, top, bottom = trigger.group(2).split('/', 2)

    url = 'memegen.link/{}/{}/{}.jpg'.format(meme, top, bottom)

    bot.say(url)
