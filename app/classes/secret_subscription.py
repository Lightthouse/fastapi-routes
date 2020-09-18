from pydantic import BaseModel


class SecretSubscription(BaseModel):
    enabled: bool
    date_start: int
    date_end: int
    generations_count: int
    generations_limit: int
