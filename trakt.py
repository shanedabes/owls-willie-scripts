#!/usr/bin/python

from sopel.module import commands
from sopel.config.types import StaticSection, ValidatedAttribute
from collections import Counter
import requests


class TraktSection(StaticSection):
    api = ValidatedAttribute('api')


def setup(bot):
    bot.config.define_section('trakt', TraktSection)
    bot.memory['trakt'] = {'hist_url': 'https://api.trakt.tv/users/{}/history',
                           'stats_url': 'https://api.trakt.tv/users/{}/stats',
                           'r_url': ('https://api.trakt.tv/users/{}/'
                                     'ratings/movies'),
                           'headers': {'Content-Type': 'application/json',
                                       'trakt-api-version': '2',
                                       'trakt-api-key': bot.config.trakt.api}}


def configure(config):
    config.define_section('trakt', TraktSection, validate=False)
    config.trakt.configure_setting('api', 'Enter trakt api')


@commands('trakt')
def trakt(bot, trigger):
    user = trigger.group(2)

    if not user:
        bot.say('No user given')
        return

    r = requests.get(bot.memory['trakt']['hist_url'].format(user),
                     headers=bot.memory['trakt']['headers'])

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

    if not user:
        bot.say('No user given')
        return

    stats_r = requests.get(bot.memory['trakt']['stats_url'].format(user),
                           headers=bot.memory['trakt']['headers'])

    if stats_r.status_code == 404:
        bot.say('User {} does not exist'.format(user))
        return

    ratings_r = requests.get(bot.memory['trakt']['r_url'].format(user),
                             headers=bot.memory['trakt']['headers'])

    stats = stats_r.json()
    ratings = ratings_r.json()
    r_counter = Counter(i['rating'] for i in ratings)
    ratings_dist = '/'.join(str(i) for i in r_counter.values())

    meta = [user,
            stats['movies']['watched'],
            stats['shows']['watched'],
            stats['episodes']['watched'],
            sum(r_counter.values()),
            ratings_dist]
    out = ('{} has watched {} films and {} shows with {} episodes. They have '
           'rated {} films with the following distribution: {}').format(*meta)

    bot.say(out)
