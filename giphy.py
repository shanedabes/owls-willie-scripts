#!/usr/bin/python

from sopel.module import commands
import giphypop
from pyshorteners import Shortener

g = giphypop.Giphy()
shortener = Shortener('Isgd')

@commands('gif')
def gif(bot, trigger):
    search = trigger.group(2) or ''
    gi = g.random_gif(search)

    if not gi:
        bot.say('NO GIFS U FUK')
    else:
        gif_url = shortener.short(gi.media_url)
        bot.say(gif_url)
