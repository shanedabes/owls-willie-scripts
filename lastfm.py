#!/usr/bin/python

from sopel.module import commands
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.db import SopelDB
import requests


class LastfmSection(StaticSection):
    api = ValidatedAttribute('api')


def setup(bot):
    bot.config.define_section('lastfm', LastfmSection)


def configure(config):
    config.define_section('lastfm', LastfmSection, validate=False)
    config.lastfm.configure_setting('api', 'Enter last.fm api: ')


@commands('fm')
def fm(bot, trigger):
    user = trigger.group(2)
    api = bot.config.lastfm.api

    if not user:
        db = SopelDB(bot.config)
        user = db.get_nick_value(trigger.nick, 'lastfm_user')
        if not user:
            bot.say('User not given or set. Use .fmset to set your user')
            return

    r = requests.get('http://ws.audioscrobbler.com/2.0/'
                     '?method=user.getrecenttracks&user={}&'
                     'api_key={}&format=json'.format(user, api))

    if 'recenttracks' not in r.json():
        bot.say('User {} not found'.format(user))
        return

    if len(r.json()['recenttracks']['track']) == 0:
        bot.say('{} hasn\'t listened to any tracks yet'.format(user))
        return

    last = r.json()['recenttracks']['track'][0]

    if '@attr' in last and last['@attr']['nowplaying'] == 'true':
        action = 'is listening to'
    else:
        action = 'last listened to'

    meta = (user, action, last['artist']['#text'], last['name'],
            last['album']['#text'])
    out = '♫ {} {} {} - {} ({}) ♫'.format(*meta)

    bot.say(out)


@commands('fmset')
def fmset(bot, trigger):
    user = trigger.group(2)

    if not user:
        bot.say('no user given')
        return

    db = SopelDB(bot.config)
    db.set_nick_value(trigger.nick, 'lastfm_user', user)

    bot.say('{}\'s last.fm user is now set as {}'.format(trigger.nick, user))
