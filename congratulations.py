#!/usr/bin/python

from sopel.module import rule


@rule(r'^[Cc]ongratulations!?')
def congratulations(bot, trigger):
    bot.say('congratulations!')
