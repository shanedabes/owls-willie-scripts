#!/usr/bin/python

from sopel.config.types import StaticSection, ListAttribute
from sopel.config import ConfigurationError


class ReplySection(StaticSection):
    rules = ListAttribute('rules')
    replies = ListAttribute('replies')


def setup(bot):
    bot.config.define_section('reply', ReplySection)

    reply.rule = bot.config.reply.rules

    if len(bot.config.reply.rules) != len(bot.config.reply.replies):
        raise ConfigurationError('Number of rules and replies must match')


def configure(config):
    config.define_section('reply', ReplySection, validate=False)
    config.reply.configure_setting('rules', 'enter rules to listen for')
    config.reply.configure_setting('replies', 'enter corresponding replies')


def reply(bot, trigger):
    rules, replies = bot.config.reply.rules, bot.config.reply.replies
    rule = trigger.args[1]
    reply = replies[rules.index(rule)]

    bot.say(reply)
