from pydantic import BaseModel
from fastapi import Body
from .secret_token_cache import SecretTokenCache


class SecretOneApplication(BaseModel):
    type: str
    subdomain: str
    client_id: str
    client_secret: str
    account_id: int
    account_name: str
    token_cache: SecretTokenCache = Body(...)
