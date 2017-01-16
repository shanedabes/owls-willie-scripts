#!/usr/bin/env python

from sopel.module import rule
from sopel.config.types import StaticSection, ListAttribute


class BLSection(StaticSection):
    blacklist = ListAttribute('blacklist')


def setup(bot):
    bot.config.define_section('blacklist', BLSection)

    bot.memory['blacklist'] = bot.config.blacklist.blacklist


def configure(config):
    config.define_section('blacklist', BLSection, validate=False)
    config.blacklist.configure_setting('blacklist', 'enter words to blacklist')


@rule('.*')
def blacklist(bot, trigger):
    words = [i for i in bot.memory['blacklist'] if i in trigger.args[1]]
    if words:
        chan = trigger.sender
        user = trigger.nick
        reason = 'don\'t say {}'.format(' or '.join(words))

        bot.write(['KICK', chan, user], reason)
