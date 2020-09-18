from pydantic import BaseModel


class SecretTokenCache(BaseModel):
    token_type: str
    expires_in: int
    access_token: str
    refresh_token: str
    expires_at: int
