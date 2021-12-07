from decorator import request_url
from configs import (
    USER_OTP_REQUEST_URL,
    USER_LOGIN_BY_OTP_URL,
    USER_LOGIN_REFRESH_TOKEN,
    USER_OTP_REQUEST_CODE_INCLUDED_URL,
    USER_VERIFY_OTP_REQUEST_CODE_INCLUDED,
)


@request_url(url=USER_OTP_REQUEST_URL)
async def async_user_otp_request(*, url: str, msisdn: int):
    pass


@request_url(url=USER_LOGIN_BY_OTP_URL)
async def async_user_login_by_otp(*, url: str, sms_code: str):
    pass


@request_url(url=USER_LOGIN_REFRESH_TOKEN)
async def async_user_login_refresh_token(*, url: str, refresh_token: str):
    pass


@request_url(url=USER_OTP_REQUEST_CODE_INCLUDED_URL)
async def async_user_otp_request_code_included(*, url: str):
    pass


@request_url(url=USER_VERIFY_OTP_REQUEST_CODE_INCLUDED)
async def async_user_verify_otp_request_code_included(*, url: str, sms_code: str):
    pass
