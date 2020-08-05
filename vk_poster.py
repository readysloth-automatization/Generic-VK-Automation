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
