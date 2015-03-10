#!/usr/bin/python

from willie.module import commands
import requests

api = '10c008753ac9b96f28f91594236141bc2390240d8fe7947a8c38f3a351c9a586'
# user = 'sharktamer'
url = ('http://api.trakt.tv/activity/user.json/{0}/{1}/episode,movie/'
       'watching,scrobble,checkin,seen?min=1')
url = ('https://api.trakt.tv/users/username/history/episodes,movies')


@commands('trakt')
def trakt(bot, trigger):
    user = trigger.group(2)
    r = requests.get(url.format(api, user)).json()

    if user is None:
        bot.say('Usage: .trakt <username>')
        return 0

    if 'status' in r:
        bot.say('Fetch failed for user {0}'.format(user))
        return 0

    if len(r['activity']) == 0:
        bot.say('{0} has no activity'.format(user))
        return 0

    last = r['activity'][0]

    out = '{}\'s most recent trakt activity: '.format(user)

    if last['type'] == 'episode':
        show = last['show']['title']
        if 'episodes' in last:
            season = last['episodes'][0]['season']
            episode = str(last['episodes'][0]['episode']).zfill(2)
            title = last['episodes'][0]['title']
        else:
            season = last['episode']['season']
            episode = str(last['episode']['number']).zfill(2)
            title = last['episode']['title']
        out += '{} {}x{}: {}'.format(show, season, episode, title)
    elif last['type'] == 'movie':
        out += last['movie']['title']

    if last['action'] == 'watching':
        out += ' (watching now)'

    bot.say(out)

