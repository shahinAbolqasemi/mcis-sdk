from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    scope: str
    token_type: str
    expires_in: int


class ClientToken(BaseModel):
    token: str
    refreshToken: str
    expires: str
    type: str


class BillInquiry(BaseModel):
    bill_id: str
    pay_id: str
    amount: int
