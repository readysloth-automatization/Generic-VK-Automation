import sys
import time
import typing
import asyncio
import datetime as d
import functools as f

from typing import Union, List, Iterable, Callable

import utils

import vkwave.api as vapi
import vkwave.client as client
import vkwave.api.token.token as t

import vkwave.bots as bots

def make_longpoll_bot(tokens: Union[str, Iterable[str]], group_id: int) -> bots.SimpleLongPollBot:
    return bots.SimpleLongPollBot(tokens=tokens, group_id=group_id)

def assign_message_handler(bot: bots.SimpleLongPollBot,
                           handler: Callable[[bots.SimpleBotEvent], None],
                           filter: bots.core.BaseFilter = None):
    if filter:
        bot.message_handler(filter)(handler)
        return
    bot.message_handler()(handler)

async def simple(event: bots.SimpleBotEvent):
    await event.answer("hello from vkwave!")

def test():
    bot = make_longpoll_bot(sys.argv[1], 196946159)
    #bot.text_filter("hello")
    assign_message_handler(bot, simple)


    bot.run_forever()
test()
