#!/usr/bin/python

from sopel.module import commands
from sopel.config.types import StaticSection, ValidatedAttribute
import requests


class TraktSection(StaticSection):
    api = ValidatedAttribute('api')


def setup(bot):
    bot.config.define_section('trakt', TraktSection)
    bot.memory['trakt'] = {'url': 'https://api.trakt.tv/users/{}/history',
                           'headers': {'Content-Type': 'application/json',
                                       'trakt-api-version': '2',
                                       'trakt-api-key': bot.config.trakt.api}}


def configure(config):
    config.define_section('trakt', TraktSection, validate=False)
    config.trakt.configure_setting('api', 'Enter trakt api')


@commands('trakt')
def trakt(bot, trigger):
    user = trigger.group(2)
    r = requests.get(bot.memory['trakt']['url'].format(user),
                     headers=bot.memory['trakt']['headers'])

    if not user:
        bot.say('No user given')
        return

    if r.status_code == 404:
        bot.say('User {} does not exist'.format(user))
        return

    if len(r.json()) == 0:
        bot.say('User {} has no history'.format(user))
        return

    last = r.json()[0]

    if last['type'] == 'episode':
        meta = [user,
                last['show']['title'],
                last['episode']['season'],
                last['episode']['number'],
                last['episode']['title']]
        out = '{} last watched: {} {}x{:02} - {}'.format(*meta)
    elif last['type'] == 'movie':
        meta = [user,
                last['movie']['title'],
                last['movie']['year']]
        out = '{} last watched: {} ({})'.format(*meta)

    bot.say(out)
