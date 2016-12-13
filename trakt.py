#!/usr/bin/python

from sopel.module import commands
from sopel.config.types import StaticSection, ValidatedAttribute
# from sopel.formatting import color, colors
import requests


class TraktSection(StaticSection):
    api = ValidatedAttribute('api')


def setup(bot):
    bot.config.define_section('trakt', TraktSection)
    bot.memory['trakt'] = {'hist_url': 'https://api.trakt.tv/users/{}/history',
                           'stats_url': 'https://api.trakt.tv/users/{}/stats',
                           'headers': {'Content-Type': 'application/json',
                                       'trakt-api-version': '2',
                                       'trakt-api-key': bot.config.trakt.api}}


def configure(config):
    config.define_section('trakt', TraktSection, validate=False)
    config.trakt.configure_setting('api', 'Enter trakt api')


@commands('trakt')
def trakt(bot, trigger):
    user = trigger.group(2)
    r = requests.get(bot.memory['trakt']['hist_url'].format(user),
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


@commands('traktstats')
def traktstats(bot, trigger):
    user = trigger.group(2)
    r = requests.get(bot.memory['trakt']['stats_url'].format(user),
                     headers=bot.memory['trakt']['headers'])

    if not user:
        bot.say('No user given')
        return

    if r.status_code == 404:
        bot.say('User {} does not exist'.format(user))
        return

    stats = r.json()

    ratings = stats['ratings']['distribution']
    ratings_dist = '/'.join(str(ratings[str(i)]) for i in range(1, 11))

    meta = [user,
            stats['movies']['watched'],
            stats['shows']['watched'],
            stats['episodes']['watched'],
            stats['ratings']['total'],
            ratings_dist]
    out = ('{} has watched {} films and {} shows with {} episodes. They have '
           '{} ratings with the following distribution: {}').format(*meta)

    bot.say(out)
