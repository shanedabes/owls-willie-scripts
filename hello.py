from willie import module
from random import choice

meanWords = ["loser", "lamer", "dum dum"]
insultees = ["SebK", "`Edd"]


@module.nickname_commands('hello')
def hi(bot, trigger):
    if trigger.nick in insultees:
        bot.say("Shut up " + choice(meanWords))
    else:
        bot.say('Hi, ' + trigger.nick)

