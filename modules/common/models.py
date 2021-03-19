from pydantic import BaseModel


class Response(BaseModel):
    status: bool
    message: str