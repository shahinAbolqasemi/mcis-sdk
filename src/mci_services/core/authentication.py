import httpx
import json
from typing import Literal
from mci_services.decorator import request_url
from mci_services.models import (
    AccessToken,
    ClientToken
)
from mci_services.utils import username_and_password_to_b64_token

from mci_services.configs import TOKEN_URL, CLIENT_AUTH_URL, VERIFY_OTP_CODE_URL, OTP_REQUEST_CODE_INCLUDED_URL


async def async_get_access_token(
        consumer_key: str,
        consumer_password: str,
        grant_type: str = 'client_credentials'
) -> AccessToken:
    headers = {'Authorization': f'Basic {username_and_password_to_b64_token(consumer_key, consumer_password)}'}
    data = {'grant_type': grant_type}
    async with httpx.AsyncClient() as client:
        resp = await client.post(url=TOKEN_URL, data=data, headers=headers)
    resp.raise_for_status()
    return AccessToken(**json.loads(resp.text))


async def async_get_client_token(
        access_token: AccessToken,
        prefer: Literal[
            'dynamic=false',
            'dynamic=true',
            'dynamic=false,code=520',
            'dynamic=true,code=520'
        ] = 'dynamic=false'
) -> ClientToken:
    headers = {
        "Accept": "application/json",
        "prefer": prefer,
        "Authorization": access_token.access_token
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url=CLIENT_AUTH_URL, headers=headers)
    resp.raise_for_status()
    return ClientToken(**json.loads(resp.text)['result']['data'])


# OTPAuthentication
async def async_user_otp_request_code_included(
        *,
        msisdn: str,
        prefer: Literal[
            'dynamic=false',
            'dynamic=true',
            'dynamic=false,code=520',
            'dynamic=true,code=520'
        ] = 'dynamic=false',
        access_token: AccessToken,
) -> int:

    data = {'msisdn': msisdn}
    headers = {
        "Accept": "application/json",
        "prefer": prefer,
        "Content-Type": "application/json",
        "Authorization": access_token.access_token
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url=OTP_REQUEST_CODE_INCLUDED_URL,
            headers=headers,
            json=data
        )
    resp.raise_for_status()
    return int(json.loads(resp.text)['result']['data']['code'])


@request_url(url=VERIFY_OTP_CODE_URL)
async def async_verify_otp_request(
        *,
        url: str,
        sms_code: int,
        username: str,
        prefer: Literal[
            'dynamic=false',
            'dynamic=true',
            'dynamic=false,code=520',
            'dynamic=true,code=520'
        ] = 'dynamic=false',
        access_token: AccessToken,
):  # TODO: ->
    headers = {
        "Accept": "application/json",
        "username": username,
        "prefer": prefer,
        "Authorization": access_token.access_token
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url=url, headers=headers)
    resp.raise_for_status()
    return json.loads(resp.text)
