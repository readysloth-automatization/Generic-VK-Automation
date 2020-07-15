import sys
import time
import typing
import asyncio
import datetime as d
import functools as f

from enum import Enum, auto

import vkwave.api as vapi
import vkwave.api.token.token as t
import vkwave.client as client
import vkwave.client.abstract as abstr
import vkwave.bots.utils.uploaders as upl


class UploaderType(Enum):
    Document = auto()
    Graffity = auto()
    Voice = auto()
    Photo = auto()
    WallPhoto = auto()
    

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

def get_uploader(uploader_type: UploaderType, api_context: vapi.APIOptionsRequestContext) -> upl.BaseUploader:
    return {
        UploaderType.Document: upl.DocUploader(api_context),
        UploaderType.Voice: upl.VoiceUploader(api_context),
        UploaderType.Photo: upl.PhotoUploader(api_context),
        UploaderType.WallPhoto: upl.WallPhotoUploader(api_context),

    }[uploader_type]

async def upload_files(files: typing.Union[list, str],
                 id: int,
                 uploader_type: UploaderType,
                 api_context: vapi.APIOptionsRequestContext) -> str:
    group_id = -id

    async def upload_one_file(file: str):
        if uploader_type == UploaderType.WallPhoto:
            return await uploader.get_attachment_from_path(file, group_id)

        server_url = await uploader.get_server(group_id)
        with open(file, 'rb') as f:
            return uploader.attachment_name(await uploader.upload(server_url, f))

    if type(files) != list:
        files = [str(files)]

    uploader = get_uploader(uploader_type, api_context)

    tasks = []
    for file in files:
        tasks.append(upload_one_file(file))

    attachments = await asyncio.gather(*tasks)
    
    return attachments
    
    
async def test():
        concrete_api = make_api_context(sys.argv[1], t.UserSyncSingleToken, client.AIOHTTPClient)
        url_arg = await upload_files(['in_deep_space.jpg','in_deep_space.jpg'],
                                     196946159,
                                     UploaderType.WallPhoto,
                                     concrete_api)
        await get_wall_post_func(196946159,
                           'тест',
                           concrete_api,
                           attachments=url_arg
                           )()
        return url_arg
            

print(asyncio.get_event_loop().run_until_complete(test()))
