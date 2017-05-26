from sopel.module import commands
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.config import ConfigurationError
import requests
import re


class SASection(StaticSection):
    user = ValidatedAttribute('sa_user')
    pw = ValidatedAttribute('sa_pass')


def setup(bot):
    bot.config.define_section('sa', SASection)

    bot.memory['sa'] = {'session': requests.Session()}

    login_url = 'http://forums.somethingawful.com/account.php?action=loginform'
    payload = {
        'action': 'login',
        'username': bot.config.sa.user,
        'password': bot.config.sa.pw
    }
    response = bot.memory['sa']['session'].post(login_url, data=payload)
    bot.memory['sa']['session'].post(login_url, data=payload)

    if response.status_code != 200:
        raise ConfigurationError('Unable to login')


def configure(config):
    config.define_section('sa', SASection, validate=False)
    config.sa.configure_setting('user', 'sa user to login as:')
    config.sa.configure_setting('pw', 'sa user password:')


@commands('sa')
def get_last_sa_post(bot, trigger):
    user = trigger.groups()[1]
    search_url = ('http://forums.somethingawful.com/'
                  'query.php?q=username%3A"{}"+&action=query')
    re_post = re.compile(r'(?:class="threadtitle"[^>]+>)([^<]+)')
    re_thread = re.compile(r'(?:class="blurb"[^>]*?>)([^<]+)')

    r = bot.memory['sa']['session'].get(search_url.format(user))

    if 'Please wait' in r.text:
        bot.say('Searching too quick!')
        return

    if 'User {} was not found'.format(user) in r.text:
        bot.say('User {0} was not found'.format(user))
        return

    if 'blurb' not in r.text:
        bot.say('{0} has no posts (what a loser)'.format(user))
        return

    thread = re_post.search(r.text).group(1)
    post = re_thread.search(r.text).group(1).strip()
    bot.say('{0}[...] ({1})'.format(post, thread))
