import sys
import asyncio

import vkwave.api as vapi
import vkwave.api.token.token as t
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
