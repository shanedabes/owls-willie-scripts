#!/usr/bin/env python

from sopel.module import rule
from sopel.config.types import StaticSection, ListAttribute, ValidatedAttribute
from random import randint


class RKSection(StaticSection):
    users = ListAttribute('randkick_users')
    reason = ValidatedAttribute('randkick_reason')
    chance = ValidatedAttribute('randkick_chance', int)


def setup(bot):
    bot.config.define_section('randkick', RKSection)

    bot.memory['randkick'] = {
        'users': bot.config.randkick.users,
        'reason': bot.config.randkick.reason,
        'chance': bot.config.randkick.chance
    }


def configure(config):
    config.define_section('randkick', RKSection, validate=False)
    config.randkick.configure_setting('users', 'users to kick')
    config.randkick.configure_setting('reason', 'reason for kick')
    config.randkick.configure_setting('chance', 'chance of kick')


@rule('.*')
def randkick(bot, trigger):
    if trigger.nick in bot.memory['randkick']['users']:
        if randint(1, bot.memory['randkick']['chance']) == 1:
            chan = trigger.sender
            user = trigger.nick
            reason = bot.memory['randkick']['reason']

            bot.write(['KICK', chan, user], reason)
