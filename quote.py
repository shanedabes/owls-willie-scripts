#!/usr/bin/python

from random import choice
from sopel.module import commands


@commands('quote')
def get_quote(bot, trigger):
    if trigger.group(2).count(' ') == 0:
        user, new_quote = trigger.group(2), None
    else:
        user, new_quote = trigger.group(2).split(' ', 1)

    if not trigger.group(2):
        bot.say('Error: a user and optionally a new quote are needed')
        return

    quotes = bot.db.get_nick_value(user, 'quotes')

    if new_quote:
        if not trigger.owner:
            bot.say('You are not the bot owner')
            return
        if not quotes:
            quotes = new_quote
        else:
            if new_quote in quotes:
                bot.say('Quote already exists')
                return
            quotes = quotes + '\x1e' + new_quote
        bot.db.set_nick_value(user, 'quotes', quotes)
        bot.say('New quote added for {}'.format(user))
        return

    if not quotes:
        bot.say('No quotes saved for {}'.format(user))
        return

    quote = choice(quotes.split('\x1e'))
    bot.say('{}: {}'.format(user, quote))
