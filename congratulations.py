#!/usr/bin/python

from willie.module import rule


@rule(r'^[Cc]ongratulations!?')
def congratulations(bot, trigger):
    bot.say('Congratulations!')

