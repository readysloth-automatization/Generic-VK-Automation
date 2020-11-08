import sys
import typing
import asyncio
import datetime as d
import functools as f

import utils

import vkwave.api as vapi
import vkwave.bots as bots
import vkwave.client as client
import vkwave.api.token.token as t

import vk_poster as vkp
import vk_responder as vkr

async def post_test():
        vk_api, made_client = utils.make_api(sys.argv[1],
                                       t.UserSyncSingleToken,
                                       client.AIOHTTPClient)
        concrete_api = utils.make_api_context(vk_api)
        url_arg = await utils.upload_files(['in_deep_space.jpg','in_deep_space.jpg'],
                                           196946159,
                                           utils.UploaderType.WallPhoto,
                                           concrete_api)
        await vkp.get_wall_post_func(196946159,
                                     'тест',
                                     concrete_api,
                                     attachments=url_arg)()
        await made_client.close()
        return url_arg
            

async def simple(event: bots.SimpleBotEvent):
    await event.answer("hello from vkwave!")

def respond_test():
    bot = vkr.make_longpoll_bot(sys.argv[1], 196946159)
    assign_message_handler(bot, simple)

    bot.run_forever()
