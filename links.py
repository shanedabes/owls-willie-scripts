#!/usr/bin/python

from sopel.module import commands
from url import find_title
import random

def send_vid(bot, url):
    bot.say(find_title(url))
    bot.say(url)

@commands('yungle')
def yungle(bot, trigger):
    send_vid(bot, 'https://youtu.be/d4vOSFB7UxM')

@commands('slaiyers')
def slaiyers(bot, trigger):
    send_vid(bot, 'https://youtu.be/NbCM1pREIDM')

@commands('spencecat')
def spencecat(bot, trigger):
    send_vid(bot, 'https://youtu.be/wycimfa5yuI')

@commands('bmo')
def bmo(bot, trigger):
    vids = [
        'fYuhBvYVAqQ',
        '-gpkYhVTRxs',
        'ixXU1fngoyI',
        'XGK0oItKR94',
        '0QRpJv1nYG4'
    ]
    send_vid(bot, 'https://youtu.be/{}'.format(random.choice(vids)))

@commands('fuk')
def fuk(bot, trigger):
    bot.say('http://is.gd/xRDJNP')
