from sopel.module import commands
from cowpy import cow

@commands('cow')
def cowsay(bot, trigger):
    cowtype = trigger.group(3)
    msg = ' '.join(trigger.group(2).split()[1:])

    try:
        c = getattr(cow, cowtype)()
    except AttributeError:
        c = cow.Small()
        msg = trigger.group(2)

    for line in c.milk(msg).splitlines():
        bot.say(line)

