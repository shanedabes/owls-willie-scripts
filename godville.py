#!/usr/bin/python

from sopel.module import commands
from sopel.db import SopelDB
import requests


@commands('god')
def godstats(bot, trigger):
    god = trigger.group(2)

    if not god:
        db = SopelDB(bot.config)
        god = db.get_nick_value(trigger.nick, 'god')
        if not god:
            bot.say('God not given or set. Use .godset to set your god')
            return

    r = requests.get('http://godvillegame.com/gods/api/{}.json'.format(god))
    hero = r.json()

    out = ('{h[godname]}\'s hero {h[name]}: '
           'A level {h[level]} {h[alignment]} {h[gender]}, '
           '{h[clan]} {h[clan_position]}, {h[arena_won]} arena wins, '
           '{h[arena_lost]} arena losses. {h[motto]}').format(h=hero)

    bot.say(out)


@commands('godset')
def godset(bot, trigger):
    god = trigger.group(2)

    if not god:
        bot.say('no god given')
        return

    db = SopelDB(bot.config)
    db.set_nick_value(trigger.nick, 'god', god)

    bot.say('{}\'s god is now set as {}'.format(trigger.nick, god))
