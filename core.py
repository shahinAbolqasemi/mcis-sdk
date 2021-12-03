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


class BillInquiryManager:
    def __init__(
            self,
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
        self.bill_type = bill_type
        self.bill_id = bill_id
        self.client_authorization = client_authorization
        self.access_token = access_token

    async def get_bill_inquiry(self):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token.access_token}",
            "C-Authorization": f"Bearer {self.client_authorization.token}",
            "prefer": "dynamic=false"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=BILL_INQUIRY_URL.format(bill_id=self.bill_id, bill_type=self.bill_type),
                                    headers=headers)
        resp.raise_for_status()
        return BillInquiry(**json.loads(resp.text)['result']['data'])

    def __call__(self, *args, **kwargs):
        return self.get_bill_inquiry()


async def main():
    from authorization import AccessTokenManager, ClientTokenManager
    atm = AccessTokenManager(CONSUMER_KEY, CONSUMER_PASSWORD)
    at = await atm.get_access_token()
    ctm = ClientTokenManager(at)
    ct = await ctm.get_client_token()
    print(await BillInquiryManager(at, ct, '9183502318').get_bill_inquiry())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
