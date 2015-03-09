import willie
from cowpy import cow

@willie.module.commands('cow')
def cowsay(bot, trigger):
    #print trigger.group(1)
    #print trigger.group(2)
    #print trigger.group(3)
    #print trigger.group(4)
    #print trigger.args
    #print trigger.event
    #print trigger.group(2)
    cowtype = trigger.group(3)
    msg = ' '.join(trigger.group(2).split()[1:])

    try:
        c = getattr(cow, cowtype)()
    except AttributeError:
        c = cow.Small()
        msg = trigger.group(2)

    for line in c.milk(msg).splitlines():
        bot.say(line)

