from sopel.module import commands
from sopel.config.types import StaticSection, ValidatedAttribute, NO_DEFAULT
from sopel.db import SopelDB
import oauth2
import json


class TwitterSection(StaticSection):
    consumer_key = ValidatedAttribute('consumer_key', default=NO_DEFAULT)
    consumer_secret = ValidatedAttribute('consumer_secret', default=NO_DEFAULT)


def configure(config):
    config.define_section('twitter', TwitterSection, validate=False)
    config.twitter.configure_setting('consumer_key',
                                     'Twitter consumer key:')
    config.twitter.configure_setting('consumer_secret',
                                     'Twitter consumer secret:')


def setup(bot):
    bot.config.define_section('twitter', TwitterSection)

    consumer = oauth2.Consumer(key=bot.config.twitter.consumer_key,
                               secret=bot.config.twitter.consumer_secret)
    client = oauth2.Client(consumer)

    bot.memory['twitter'] = {'client': client}


@commands('twit')
def twit(bot, trigger):
    user = trigger.group(2)
    if not user:
        db = SopelDB(bot.config)
        user = db.get_nick_value(trigger.nick, 'twit_user')
        if not user:
            bot.say('User not given or set. Use .twitset to set your user')
            return

    url = ('https://api.twitter.com/1.1/statuses/'
           'user_timeline.json?screen_name={}').format(user)

    response, content = bot.memory['twitter']['client'].request(url)
    content_json = json.loads(content.decode('utf-8'))

    if response['status'] == '401':
        bot.say('User {}\'s tweets are private'.format(user))
        return

    if response['status'] == '404':
        bot.say('User {} not found'.format(user))
        return

    last = content_json[0]

    message = ('[Twitter] {last[text]} | {last[user][name]} '
               '(@{last[user][screen_name]}) | {last[retweet_count]} RTs '
               '| {last[favorite_count]} ♥s').format(last=last)

    bot.say(message)


@commands('twitset')
def fmset(bot, trigger):
    user = trigger.group(2)

    if not user:
        bot.say('no user given')
        return

    db = SopelDB(bot.config)
    db.set_nick_value(trigger.nick, 'twit_user', user)

    bot.say('{}\'s twitter user is now set as {}'.format(trigger.nick, user))
