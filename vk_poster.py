import sys
import time
import typing
import asyncio
import datetime as d
import functools as f

import utils

import vkwave.api as vapi
import vkwave.client as client
import vkwave.api.token.token as t

def get_wall_post_func(id: int,
                       message: str,
                       api_context: vapi.APIOptionsRequestContext,
                       user: bool = False,
                       attachments: list = None,
                       date: d.datetime = None) -> typing.Callable:

    wall_post_method = f.partial(api_context.wall.post,
                                 message=message,
                                 attachments=attachments,
                                 publish_date=int(date.timestamp()) if date else None
                                 )
    if user:
        return f.partial(wall_post_method, owner_id=id)
    else:
        return f.partial(wall_post_method, owner_id=-id)

async def test():
        vk_api, made_client = utils.make_api(sys.argv[1],
                                       t.UserSyncSingleToken,
                                       client.AIOHTTPClient)
        concrete_api = utils.make_api_context(vk_api)
        url_arg = await utils.upload_files(['in_deep_space.jpg','in_deep_space.jpg'],
                                     196946159,
                                     utils.UploaderType.WallPhoto,
                                     concrete_api)
        await get_wall_post_func(196946159,
                           'тест',
                           concrete_api,
                           attachments=url_arg
                           )()
        await made_client.close()
        return url_arg
            

print(asyncio.get_event_loop().run_until_complete(test()))
