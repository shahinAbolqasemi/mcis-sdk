import httpx
import json
from typing import Literal
from models import (
    AccessToken,
    ClientToken,
    BillInquiry
)

from configs import BILL_INQUIRY_URL, CONSUMER_KEY, CONSUMER_PASSWORD


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
    pass

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
