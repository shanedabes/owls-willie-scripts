#!/usr/bin/python

from random import choice
from sopel.config.types import StaticSection, ListAttribute


class LinksSection(StaticSection):
    names = ListAttribute('names')


def setup(bot):
    bot.config.define_section('links', LinksSection)

    get_link.commands = bot.config.links.names


def configure(config):
    config.define_section('links', LinksSection, validate=False)
    config.links.configure_setting('names', 'enter links commands to set up')


def get_link(bot, trigger):
    command, new_link = trigger.group(1), trigger.group(2)

    links = bot.db.get_nick_value(bot.nick, command)

    if new_link:
        if not trigger.owner:
            bot.say('You are not the bot owner')
            return
        if not links:
            links = ''
        if new_link in links:
            bot.say('Link already exists')
            return
        bot.db.set_nick_value(bot.nick, command, links + '\x1e' + new_link)
        bot.say('New link added for .{} command'.format(command))
        return

    if not links:
        bot.say('No links set for {}'.format(command))
        return

    link = choice(links.split('\x1e'))
    bot.say(link)
