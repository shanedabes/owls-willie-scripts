from sopel.module import commands, require_privmsg
from sopel.db import SopelDB
import stravalib.client
from stravalib import unithelper


def seconds_to_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return hours, minutes, seconds


def strava_lastact(bot, trigger, client):
    act = next(client.get_activities())

    name = act.name
    act_type = act.type
    distance = unithelper.kilometers(act.distance)
    start = act.start_date_local.strftime('%-d %B %-H:%m')
    time = '{:02}:{:02}:{:02}'.format(*seconds_to_time(act.moving_time.seconds))
    achievements = act.achievement_count

    tokens = [trigger.nick, name, act_type, distance, time, start, achievements]
    out = '{}\'s last activity: {} ({}) {} ({}) on {} ({} ☺️)'.format(*tokens)
    bot.say(out)
    bot.say('https://www.strava.com/activities/{}'.format(act.id))


def strava_bikes(bot, trigger, client):
    athlete = client.get_athlete()

    for i in athlete.bikes:
        bot.say('{}: {}'.format(i.name, unithelper.kilometers(i.distance)))


def strava_koms(bot, trigger, client):
    athlete = client.get_athlete()
    koms = client.get_athlete_koms(athlete.id)

    for kom in koms:
        name = kom.name
        kom_type = kom.segment.activity_type
        distance = unithelper.kilometers(kom.distance)
        time = kom.moving_time
        printtime = '{:02}:{:02}:{:02}'.format(*seconds_to_time(time.seconds))
        efforts = kom.segment.leaderboard.effort_count
        if len(kom.segment.leaderboard.entries) > 1:
            next_time = kom.segment.leaderboard.entries[1].moving_time
            diff = next_time - time
        else:
            diff = time - time
        printdiff = '{:02}:{:02}:{:02}'.format(*seconds_to_time(diff.seconds))

        tokens = [name, kom_type, efforts, distance, printtime, printdiff]
        bot.say('{} ({}): 1/{} - {} in {} - {} faster'.format(*tokens))


def strava_help(bot, trigger, client):
    bot.say('Invalid action')
    bot.say('Pick from: lastact, help, bikes, koms')


@commands('strava')
def strava(bot, trigger):
    db = SopelDB(bot.config)
    strava_token = db.get_nick_value(trigger.nick, 'strava_token')
    if not strava_token:
        bot.say('Strava token not set. Use .stravaset (through PMs) to set')
        return

    client = stravalib.client.Client()
    client.access_token = strava_token

    action = trigger.group(2)
    action_funs = {
        'lastact': strava_lastact,
        'bikes': strava_bikes,
        'koms': strava_koms
    }
    action_fun = action_funs.get(action, strava_help)
    action_fun(bot, trigger, client)


@require_privmsg
@commands('stravaset')
def stravaset(bot, trigger):
    strava_token = trigger.group(2)

    if not strava_token:
        bot.say('no access token given')
        bot.say('Generate using https://stravacli-dlenski.rhcloud.com')
        return

    db = SopelDB(bot.config)
    db.set_nick_value(trigger.nick, 'strava_token', strava_token)

    bot.say('{}\'s token is now set as {}'.format(trigger.nick, strava_token))
