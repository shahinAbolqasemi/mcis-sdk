from decorator import request_url
from configs import CHARGE_BALANCE_INQUIRY_URL
from typing import Literal
import httpx
import json
from models import AccessToken


@request_url(url=CHARGE_BALANCE_INQUIRY_URL)
async def async_balance_inquiry(
        *,
        url: str,
        access_token: AccessToken,
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
        "Authorization": access_token.access_token
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url=url, headers=headers)
    resp.raise_for_status()
    json_response = json.loads(resp.text)
    return json_response['result']['data']['balance']
