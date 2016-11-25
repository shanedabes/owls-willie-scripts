#!/usr/bin/env python

from sopel.module import commands
import requests


@commands('joke')
def joke(bot, trigger):
    r = requests.get('http://tambal.azurewebsites.net/joke/random')
    joke = r.json()['joke']
    bot.say(joke)
