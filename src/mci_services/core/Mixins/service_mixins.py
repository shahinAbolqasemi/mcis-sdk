import httpx
import json
from typing import Literal, Tuple
from mci_services.decorator import request_url
from mci_services.models import (
    ClientToken,
    BillInquiry, LoggedInUser, RefreshTokenLoggedInUser
)

from mci_services.configs import CLIENT_AUTH_URL, VERIFY_OTP_CODE_URL, OTP_REQUEST_CODE_INCLUDED_URL, \
    BILL_INQUIRY_URL, RBT_INQUIRY_URL, USER_LOGIN_REFRESH_TOKEN_URL, USER_OTP_REQUEST_URL, \
    USER_OTP_REQUEST_CODE_INCLUDED_URL, USER_VERIFY_OTP_REQUEST_CODE_INCLUDED, USER_LOGIN_BY_OTP_URL, \
    CHARGE_BALANCE_INQUIRY_URL


class BillServiceMixin:
    @request_url(url=BILL_INQUIRY_URL)
    async def async_get_bill_inquiry(
            self,
            *,
            bill_id: str,
            bill_type: Literal[
                "gas",
                "electricity",
                "water",
                "rahvar",
                "mobile",
                "mobileHotbill",
                "pstn",
                "pstnHotbill"
            ] = 'mobile',
            url: str,
            client_authorization: ClientToken = None
    ):
        headers = {
            "Accept": "application/json",
            "Authorization": self.access_token.access_token,
            "C-Authorization": client_authorization.token if client_authorization else (await self.client_token).token,
            "prefer": "dynamic=false"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=url,
                                    headers=headers)
        resp.raise_for_status()
        return BillInquiry(**json.loads(resp.text)['result']['data'])


class AuthenticationServiceMixin:
    async def async_get_client_token(
            self,
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
            "Authorization": self.access_token.access_token
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=CLIENT_AUTH_URL, headers=headers)
        resp.raise_for_status()
        return ClientToken(**json.loads(resp.text)['result']['data'])

    # OTPAuthentication
    async def async_user_otp_request_code_included(
            self,
            *,
            msisdn: str,
            prefer: Literal[
                'dynamic=false',
                'dynamic=true',
                'dynamic=false,code=520',
                'dynamic=true,code=520'
            ] = 'dynamic=false',
    ) -> int:
        data = {'msisdn': msisdn}
        headers = {
            "Accept": "application/json",
            "prefer": prefer,
            "Content-Type": "application/json",
            "Authorization": self.access_token.access_token
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
            self,
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
    ):  # TODO: ->
        headers = {
            "Accept": "application/json",
            "username": username,
            "prefer": prefer,
            "Authorization": self.access_token.access_token
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=url, headers=headers)
        resp.raise_for_status()
        return json.loads(resp.text)


class RBTServiceMixin:
    @request_url(url=RBT_INQUIRY_URL)
    async def async_rbt_inquiry(
            self,
            *,
            url: str,
            acl_id: str,
            prefer: Literal[
                'dynamic=false',
                'dynamic=true',
                'dynamic=false,code=520',
                'dynamic=true,code=520'
            ] = 'dynamic=false',
            x_authorization: str
    ) -> Literal['ACTIVE', 'INACTIVE']:
        headers = {
            "Accept": "application/json; charset=UTF-8",
            "X-Authorization": x_authorization,
            "prefer": prefer,
            "Authorization": self.access_token.access_token
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=url, headers=headers)
        resp.raise_for_status()
        json_response = json.loads(resp.text)
        return json_response['result']['data']['status']


class UserAuthServiceMixin:
    @request_url(url=USER_OTP_REQUEST_URL)
    async def async_user_otp_request(
            self,
            *,
            url: str,
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
        :param msisdn: No zero phone number
        :return: tuple of status of send OTP request and message
        """
        headers = {
            "Accept": "application/json",
            "prefer": prefer,
            "Authorization": self.access_token.access_token
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
            self,
            *,
            url: str,
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
            "Authorization": self.access_token.access_token
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=url, headers=headers, params=querystring)
        resp.raise_for_status()
        json_response = json.loads(resp.text)
        return LoggedInUser(**json_response['result']['data'])

    @request_url(url=USER_LOGIN_REFRESH_TOKEN_URL)
    async def async_user_login_refresh_token(
            self,
            *,
            url: str,
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
            "Authorization": self.access_token.access_token,
            "prefer": prefer
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=url, headers=headers)
        resp.raise_for_status()
        json_response = json.loads(resp.text)
        return RefreshTokenLoggedInUser(**json_response['result']['data'])

    @request_url(url=USER_OTP_REQUEST_CODE_INCLUDED_URL)
    async def async_user_otp_request_code_included(
            self,
            *,
            url: str,
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
            "Authorization": self.access_token.access_token
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
            self,
            *,
            url: str,
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
            "Authorization": self.access_token.access_token
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=url, headers=headers)

        resp.raise_for_status()
        json_response = json.loads(resp.text)
        ok = 200 <= json_response['status']['code'] < 300
        message = json_response['result']['status']['message']
        return ok, message


class EtopupMixin:
    @request_url(url=CHARGE_BALANCE_INQUIRY_URL)
    async def async_balance_inquiry(
            self,
            *,
            url: str,
            acl_id: str,
            prefer: Literal[
                'dynamic=false',
                'dynamic=true',
                'dynamic=false,code=520',
                'dynamic=true,code=520'
            ] = 'dynamic=false',
            x_authorization: str
    ) -> int:
        headers = {
            "Accept": "application/json",
            "x-authorization": x_authorization,
            "prefer": prefer,
            "Authorization": self.access_token.access_token
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=url, headers=headers)
        resp.raise_for_status()
        json_response = json.loads(resp.text)
        return json_response['result']['data']['balance']