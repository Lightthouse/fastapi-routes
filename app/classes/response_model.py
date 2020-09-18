from pydantic import BaseModel


class ResponseModel(BaseModel):
    is_complete: bool = True
    error: str = ''
