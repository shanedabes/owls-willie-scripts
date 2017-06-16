#!/usr/bin/env python

from sopel.module import commands
import requests


def escape(text):
    trans = [(' ', '_'), ('?', '~q'), ('#', '~h'), ('/', '~s'), ('"', '\'\'')]

    for a, b in trans:
        text = text.replace(a, b)

    return text


@commands('meme')
def meme(bot, trigger):
    if not trigger.group(2) or trigger.group(2).count('/') < 2:
        bot.say('Usage: .meme meme_type/top_text/bottom_text')
        bot.say('List of meme templates: https://memegen.link/api/templates/')
        return

    meme, top, bottom = [escape(i) for i in trigger.group(2).split('/', 2)]

    check = requests.get('https://memegen.link/api/templates/{}'.format(meme))
    if check.status_code != 200:
        bot.say('Meme not recognised')
        bot.say('List of meme templates: https://memegen.link/api/templates/')
        return

    url = 'https://memegen.link/{}/{}/{}.jpg'.format(meme, top, bottom)

    bot.say(url)
