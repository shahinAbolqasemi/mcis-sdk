from pydantic import BaseModel, validator, Field, root_validator
from typing import List, Literal, Optional
import datetime


class AccessToken(BaseModel):
    access_token: str
    scope: str
    token_type: str
    expires_in: int

    @root_validator
    def check_access_token(cls, values):
        values['access_token'] = f"{values.get('token_type')} {values.get('access_token')}"
        return values


class ClientToken(BaseModel):
    token: str
    refreshToken: str
    expires: datetime.datetime
    type: str

    @root_validator
    def check_token(cls, values):
        values['token'] = f"{values.get('type')} {values.get('token')}"
        return values

    @validator('expires')
    def remove_datetime_tz(cls, value):
        return value.replace(tzinfo=None)


class BillInquiry(BaseModel):
    bill_id: str
    pay_id: str
    amount: int


class ACL(BaseModel):
    id: str
    msisdn: str
    sim_type: Literal['PREPAID', 'POSTPAID'] = Field(alias='simType')


class UserLoginSession(BaseModel):
    id: str
    key: str
    prime: str


class LoggedInUser(BaseModel):
    id: str
    acl: List[ACL]
    expires_in: datetime.datetime = Field(alias='expiresIn')
    refresh_token: str = Field(alias='refreshToken')
    session: Optional[UserLoginSession]
    signup: bool
    token: str
    type: str

    @root_validator
    def check_token(cls, values):
        values['token'] = f"{values.get('type')} {values.get('token')}"
        return values

    @validator('expires_in')
    def remove_datetime_tz(cls, value):
        return value.replace(tzinfo=None)
