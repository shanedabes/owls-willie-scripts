#!/usr/bin/python

from sopel.module import commands
import requests
# from operator import itemgetter


@commands('steam')
def steam(bot, trigger):
# def steam(username):
    username = trigger.group(2)

    resolve_vanity_api_url = ('http://api.steampowered.com/ISteamUser/'
                              'ResolveVanityURL/v0001/'
                              '?key=C11F4BCC93488695F09B7C6ADBCF63B0'
                              '&steamid=76561197960434622'
                              '&vanityurl={}&format=json')
    steam_id_request = requests.get(resolve_vanity_api_url.format(username))
    steam_id = steam_id_request.json()['response']['steamid']

    recent_games_api_url = ('http://api.steampowered.com/IPlayerService/'
                            'GetRecentlyPlayedGames/v0001/'
                            '?key=C11F4BCC93488695F09B7C6ADBCF63B0'
                            '&steamid={}&format=json')
    recent_games_request = requests.get(recent_games_api_url.format(steam_id))
    last_game = recent_games_request.json()['response']['games'][0]
    # game_name, play_time = itemgetter('name', 'playtime_2weeks')(last_game)
    game_name = last_game['name']

    # print play_time
    # print unicode(game_name)

    # print last_game
    # print last_game[u'name']
    # print u'{}\'s last played game: {}'.format(username,
    # game_name.encode('cp850', errors='ignore'))
    out = u'{}\'s last played game: {}'.format(username, game_name)

    bot.say(out)

    # return game_name

# print steam('sharktamer')
# steam('sharktamer')
