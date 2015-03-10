from willie import module
from random import choice

meanWords = ["loser", "lamer", "dum dum"]
insultees = ["SebK", "`Edd"]


@module.nickname_commands('hello')
@module.example('{} hello'.format(bot.nick), 'Hi {}'.format(trigger.nick))
def hi(bot, trigger):
    if trigger.nick in insultees:
        bot.say("Shut up " + choice(meanWords))
    else:
        bot.say('Hi, ' + trigger.nick)

if __name__ == '__main__':
    from willie.test_tools import run_example_tests
    run_example_tests(__file__)

