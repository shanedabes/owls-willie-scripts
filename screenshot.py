#!/usr/bin/python

from sopel.module import commands
from sopel.config.types import StaticSection, ValidatedAttribute
from imgurpython import ImgurClient
# import requests

class SsSection(StaticSection):
    tws_api = ValidatedAttribute('tws_api')
    iclient_id = ValidatedAttribute('client_id')
    iclient_secret = ValidatedAttribute('client_secret')


def setup(bot):
    bot.config.define_section('ss', SsSection)

    bot.memory['ss'] = {'tws_api': bot.config.ss.tws_api,
                        'client_id': bot.config.ss.iclient_id,
                        'client_secret': bot.config.ss.iclient_secret}


def configure(config):
    config.define_section('ss', SsSection, validate=False)
    config.ss.configure_setting('tws_api', 'Enter thumbnail.ws api:')
    config.ss.configure_setting('iclient_id', 'Enter imgur client id:')
    config.ss.configure_setting('iclient_secret', 'Enter imgur client secret:')


@commands('ss')
def screenshot(bot, trigger):
    # bot.say(str(bot.memory['last_seen_url'][trigger.sender]))

    tws_api = bot.config.ss.tws_api
    url_template = ('https://api.thumbnail.ws/api/{}/thumbnail/get'
                    '?url={}&width=640')

    if trigger.group(2):
        url = trigger.group(2)
    else:
        if trigger.sender in bot.memory['last_seen_url']:
            url = bot.memory['last_seen_url'][trigger.sender]
        else:
            bot.say('Usage: .ss page_url')
            return

    iclient = ImgurClient(bot.config.ss.iclient_id,
                          bot.config.ss.iclient_secret)
    iurl = iclient.upload_from_url(url_template.format(tws_api, url))['link']

    bot.say(iurl)
