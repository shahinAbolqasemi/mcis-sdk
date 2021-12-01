import base64
import httpx
import json
from typing import Literal
from models import (
    AccessToken,
    ClientToken
)

from configs import TOKEN_URL, CLIENT_AUTH_URL

CONSUMER_KEY = "Y365qfDj6OZ0rzpTwckKux25HSsa"
CONSUMER_PASSWORD = "k4EyWgYjXdvbcnbpvzQcoJWMmFYa"

class AccessTokenManager:
    def __init__(self, consumer_key: str, consumer_password: str, grant_type: str = 'client_credentials'):
        self.grant_type = grant_type
        self.consumer_key = consumer_key
        self.consumer_password = consumer_password
        self.b64_token = self.to_b64_token(consumer_key, consumer_password)

    @staticmethod
    def to_b64_token(consumer_key, consumer_password):
        return base64.b64encode(f'{consumer_key}:{consumer_password}'.encode()).decode()

    async def get_access_token(self) -> AccessToken:
        headers = {'Authorization': f'Basic {self.b64_token}'}
        data = {'grant_type': self.grant_type}
        async with httpx.AsyncClient() as client:
            resp = await client.post(url=TOKEN_URL, data=data, headers=headers)
        resp.raise_for_status()
        return AccessToken(**json.loads(resp.text))

    def __call__(self, *args, **kwargs):
        return self.get_access_token()


class ClientTokenManager:
    def __init__(
            self,
            access_token: AccessToken,
            prefer: Literal[
                'dynamic=false',
                'dynamic=true',
                'dynamic=false,code=520',
                'dynamic=true,code=520'
            ] = 'dynamic=false'
    ):
        self.access_token = access_token
        self.prefer = prefer

    async def get_client_token(self) -> ClientToken:
        headers = {
            "Accept": "application/json",
            "prefer": self.prefer,
            "Authorization": f"Bearer {self.access_token.access_token}"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=CLIENT_AUTH_URL, headers=headers)
        resp.raise_for_status()
        return ClientToken(**json.loads(resp.text)['result']['data'])

    def __call__(self, *args, **kwargs):
        return self.get_client_token()
