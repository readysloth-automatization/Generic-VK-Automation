import sys
import time
import typing
import asyncio
import datetime as d
import functools as f

import vkwave.api as vapi
import vkwave.api.token.token as t
import vkwave.client as client
import vkwave.client.abstract as abstr

def make_token(token: str, token_type: t.AnyABCToken) -> t.AnyABCToken:
    return token_type(t.Token(token))

def make_api(token: str,
             token_type: t.AnyABCToken,
             client_type: abstr.AbstractAPIClient) -> vapi.API:
    return vapi.API(tokens=make_token(token, token_type),
                      clients=client_type())

def make_api_context(token: str,
                     token_type: t.AnyABCToken,
                     client_type: abstr.AbstractAPIClient) -> vapi.APIOptionsRequestContext:
    return make_api(token, token_type, client_type).get_context()

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
