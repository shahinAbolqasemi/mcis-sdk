from mci_services.mixins.service_mixins import AuthenticationServiceMixin, BillServiceMixin, UserAuthServiceMixin, \
    EtopupMixin
from mci_services.core.authentication import async_get_access_token
from mci_services.models import (
    AccessToken,
)


class ServiceApplication(
    AuthenticationServiceMixin,
    BillServiceMixin,
    UserAuthServiceMixin,
    EtopupMixin
):
    def __init__(self, access_token: AccessToken, name: str = None):
        self.access_token = access_token

    @classmethod
    async def create_application(cls, consumer_key: str, consumer_password: str):
        access_token = await async_get_access_token(consumer_key, consumer_password)
        return cls(access_token=access_token)

    @property
    async def client_token(self):
        return await self.async_get_client_token()


async def main():
    sapp = await ServiceApplication.create_application(
        consumer_key="Y365qfDj6OZ0rzpTwckKux25HSsa",
        consumer_password="k4EyWgYjXdvbcnbpvzQcoJWMmFYa"
    )
    print(await sapp.async_get_bill_inquiry(bill_id='9183502318'))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
