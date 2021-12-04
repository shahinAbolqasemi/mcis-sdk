import httpx
import json
from typing import Literal
from models import (
    AccessToken,
    ClientToken,
    BillInquiry
)

from configs import BILL_INQUIRY_URL

CONSUMER_KEY = "Y365qfDj6OZ0rzpTwckKux25HSsa"
CONSUMER_PASSWORD = "k4EyWgYjXdvbcnbpvzQcoJWMmFYa"


async def async_get_bill_inquiry(
        access_token: AccessToken,
        client_authorization: ClientToken,
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
        ] = 'mobile'
):
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token.access_token}",
        "C-Authorization": f"Bearer {client_authorization.token}",
        "prefer": "dynamic=false"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url=BILL_INQUIRY_URL.format(bill_id=bill_id, bill_type=bill_type),
                                headers=headers)
    resp.raise_for_status()
    return BillInquiry(**json.loads(resp.text)['result']['data'])


async def main():
    from authorization import async_get_access_token, async_get_client_token, async_verify_otp_request, async_user_otp_request_code_included
    at = await async_get_access_token(CONSUMER_KEY, CONSUMER_PASSWORD)
    ct = await async_get_client_token(at)
    # print(await async_get_bill_inquiry(at, ct, '9122222222'))
    at = await async_get_access_token(consumer_key='ke2jumSLt67TNoY_TUQS7Wx0fDga', consumer_password='XPG9s3BGmzpKle_LM9DHFQyCpk4a')
    code = await async_user_otp_request_code_included(access_token=at, msisdn='9338531066')
    print(await async_verify_otp_request(sms_code=code, username='9338531066', access_token=at))

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
