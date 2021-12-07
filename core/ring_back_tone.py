from decorator import request_url
from configs import RBT_INQUIRY_URL
from typing import Literal


@request_url(url=RBT_INQUIRY_URL)
async def async_rbt_inquiry(
        *,
        url: str,
        acl_id: str,
        prefer: Literal[
            'dynamic=false',
            'dynamic=true',
            'dynamic=false,code=520',
            'dynamic=true,code=520'
        ] = 'dynamic=false',
        x_authorization:  str):
    pass