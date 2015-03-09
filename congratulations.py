#!/usr/bin/python

import willie


@willie.module.rule(r'^[Cc]ongratulations!?')
def congratulations(bot, trigger):
    bot.say('congratulations!')

