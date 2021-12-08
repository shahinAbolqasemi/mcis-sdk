from typing import Tuple, Literal
from mci_services.decorator import request_url
import httpx
import json
from mci_services.configs import (
    USER_OTP_REQUEST_URL,
    USER_LOGIN_BY_OTP_URL,
    USER_LOGIN_REFRESH_TOKEN_URL,
    USER_OTP_REQUEST_CODE_INCLUDED_URL,
    USER_VERIFY_OTP_REQUEST_CODE_INCLUDED,
)
from mci_services.models import AccessToken, LoggedInUser, RefreshTokenLoggedInUser


@request_url(url=USER_OTP_REQUEST_URL)
async def async_user_otp_request(
        *,
        url: str,
        access_token: AccessToken,
        prefer: Literal[
            'dynamic=false',
            'dynamic=true',
            'dynamic=false,code=520',
            'dynamic=true,code=520'
        ] = 'dynamic=false',
        msisdn: int
) -> Tuple[bool, str]:
    """
    :param prefer: 
    :param url: string URL
    :param access_token:
    :param msisdn: No zero phone number
    :return: tuple of status of send OTP request and message
    """
    headers = {
        "Accept": "application/json",
        "prefer": prefer,
        "Authorization": access_token.access_token
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url=url, headers=headers)
    resp.raise_for_status()
    json_response = json.loads(resp.text)
    ok = 200 <= json_response['status']['code'] < 300
    message = json_response['result']['status']['message']
    return ok, message


@request_url(url=USER_LOGIN_BY_OTP_URL)
async def async_user_login_by_otp(
        *,
        url: str,
        access_token: AccessToken,
        username: str,
        prefer: Literal[
            'dynamic=false',
            'dynamic=true',
            'dynamic=false,code=520',
            'dynamic=true,code=520'
        ] = 'dynamic=false',
        sms_code: str
) -> LoggedInUser:
    # Corresponding Str Boolean
    csb = {
        True: 'true',
        False: 'false'
    }
    querystring = {"mcisubs": csb[True]}

    headers = {
        "Accept": "application/json; charset=utf-8",
        "prefer": prefer,
        "username": username,
        "Authorization": access_token.access_token
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url=url, headers=headers, params=querystring)
    resp.raise_for_status()
    json_response = json.loads(resp.text)
    return LoggedInUser(**json_response['result']['data'])


@request_url(url=USER_LOGIN_REFRESH_TOKEN_URL)
async def async_user_login_refresh_token(
        *,
        url: str,
        access_token: AccessToken,
        prefer: Literal[
            'dynamic=false',
            'dynamic=true',
            'dynamic=false,code=520',
            'dynamic=true,code=520'
        ] = 'dynamic=false',
        refresh_token: str
) -> RefreshTokenLoggedInUser:
    headers = {
        "Accept": "application/json",
        "Authorization": access_token.access_token,
        "prefer": prefer
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url=url, headers=headers)
    resp.raise_for_status()
    json_response = json.loads(resp.text)
    return RefreshTokenLoggedInUser(**json_response['result']['data'])


@request_url(url=USER_OTP_REQUEST_CODE_INCLUDED_URL)
async def async_user_otp_request_code_included(
        *, url:
        str, access_token: AccessToken,
        prefer: Literal[
            'dynamic=false',
            'dynamic=true',
            'dynamic=false,code=520',
            'dynamic=true,code=520'
        ] = 'dynamic=false',
        msisdn: str
) -> Tuple[str, str]:
    payload = {"msisdn": msisdn}
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "prefer": prefer,
        "Authorization": access_token.access_token
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url=url, headers=headers, json=payload)
    resp.raise_for_status()
    json_response = json.loads(resp.text)
    code = json_response['result']['data']['code']
    message = json_response['result']['status']['message']
    return code, message


@request_url(url=USER_VERIFY_OTP_REQUEST_CODE_INCLUDED)
async def async_user_verify_otp_request_code_included(
        *, url: str,
        access_token: AccessToken,
        sms_code: str,
        username: str,
        prefer: Literal[
            'dynamic=false',
            'dynamic=true',
            'dynamic=false,code=520',
            'dynamic=true,code=520'
        ] = 'dynamic=false',
) -> Tuple[bool, str]:
    headers = {
        "Accept": "application/json",
        "username": username,
        "prefer": prefer,
        "Authorization": access_token.access_token
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url=url, headers=headers)

    resp.raise_for_status()
    json_response = json.loads(resp.text)
    ok = 200 <= json_response['status']['code'] < 300
    message = json_response['result']['status']['message']
    return ok, message
