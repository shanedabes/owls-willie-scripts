#!/usr/bin/python

import random


links = {
    'yungle': 'https://youtu.be/d4vOSFB7UxM',
    'slaiyers': 'https://youtu.be/NbCM1pREIDM',
    'spencecat': 'https://youtu.be/wycimfa5yuI',
    'bmo': {
        'bmo chop': 'https://youtu.be/fYuhBvYVAqQ',
        'bmo friendship song': 'https://youtu.be/dDkvgva_u58',
        'bmo pregnant song': 'https://youtu.be/sEDVop64UmM',
        'bmo and football': 'https://youtu.be/XGK0oItKR94',
        'bmo changing batteries': 'https://youtu.be/0QRpJv1nYG4'
    },
    'fuk': 'http://is.gd/xRDJNP'
}


def out(bot, trigger):
    item = links[trigger.group(1)]
    if isinstance(item, str):
        bot.say(item)
    else:
        name, url = random.choice(list(item.items()))
        bot.say('{} - {}'.format(name, url))

out.commands = list(links.keys())
