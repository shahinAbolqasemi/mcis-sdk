import httpx
import json
from mci_services.models import (
    AccessToken,
)
from mci_services.utils import username_and_password_to_b64_token

from mci_services.configs import TOKEN_URL


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
