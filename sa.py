from sopel.module import commands
import requests
import re

url = ('http://forums.somethingawful.com/query.php?q=username%3A"{0}"+&action=qu'
        'ery&forums%5B%5D=-1&forums%5B%5D=48&forums%5B%5D=1&forums%5B%5D=155&f'
        'orums%5B%5D=214&forums%5B%5D=26&forums%5B%5D=268&forums%5B%5D=51&foru'
        'ms%5B%5D=44&forums%5B%5D=259&forums%5B%5D=146&forums%5B%5D=145&forums'
        '%5B%5D=93&forums%5B%5D=234&forums%5B%5D=103&forums%5B%5D=191&forums%5'
        'B%5D=267&forums%5B%5D=192&forums%5B%5D=158&forums%5B%5D=162&forums%5B'
        '%5D=211&forums%5B%5D=200&forums%5B%5D=46&forums%5B%5D=22&forums%5B%5D'
        '=170&forums%5B%5D=202&forums%5B%5D=265&forums%5B%5D=219&forums%5B%5D='
        '122&forums%5B%5D=181&forums%5B%5D=248&forums%5B%5D=175&forums%5B%5D=1'
        '77&forums%5B%5D=179&forums%5B%5D=183&forums%5B%5D=244&forums%5B%5D=24'
        '2&forums%5B%5D=161&forums%5B%5D=167&forums%5B%5D=91&forums%5B%5D=236&'
        'forums%5B%5D=124&forums%5B%5D=132&forums%5B%5D=90&forums%5B%5D=218&fo'
        'rums%5B%5D=152&forums%5B%5D=31&forums%5B%5D=210&forums%5B%5D=247&foru'
        'ms%5B%5D=151&forums%5B%5D=133&forums%5B%5D=182&forums%5B%5D=150&forum'
        's%5B%5D=104&forums%5B%5D=130&forums%5B%5D=144&forums%5B%5D=27&forums%'
        '5B%5D=215&forums%5B%5D=255&forums%5B%5D=153&forums%5B%5D=61&forums%5B'
        '%5D=77&forums%5B%5D=85&forums%5B%5D=43&forums%5B%5D=241&forums%5B%5D='
        '188&forums%5B%5D=49&forums%5B%5D=21&forums%5B%5D=264&forums%5B%5D=115'
        '&forums%5B%5D=176&forums%5B%5D=229&forums%5B%5D=25')
login_url = 'http://forums.somethingawful.com/account.php?action=loginform'
payload = {'action': 'login', 'username': 'sharktamer', 'password': '5pac3k3v1n'}
re_post = re.compile(r'(?:class="threadtitle"[^>]+>)([^<]+)')
re_thread = re.compile(r'(?:class="blurb"[^>]*>)([^<]+)')

@commands('sa')
def get_last_sa_post(bot, trigger):
    with requests.Session() as s:
        user = trigger.groups()[1]
        s.post(login_url, data=payload)

        r = s.get(url.format(user))

        if 'Please wait' in r.text:
            bot.say('Searching too quick!')
            return
            
        if 'action=results' not in r.url:
            bot.say('user {0} not found'.format(user))
            return

        if 'blurb' not in r.text:
            bot.say('{0} has no posts (what a loser)'.format(user))
            return

        thread = re_post.search(r.text).group(1)
        post = re_thread.search(r.text).group(1).strip()
        bot.say('{0}[...] ({1})'.format(post, thread))

