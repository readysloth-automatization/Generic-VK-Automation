import typing
import asyncio

from enum import Enum, auto

import vkwave.api as vapi
import vkwave.client as client
import vkwave.api.token.token as t
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
    made_client = client_type()
    return vapi.API(tokens=make_token(token,
                                      token_type),
                    clients=made_client), made_client

def make_api_context(vk_api: vapi.API) -> vapi.APIOptionsRequestContext:
    return vk_api.get_context()

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
    
