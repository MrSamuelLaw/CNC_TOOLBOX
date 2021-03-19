from pydantic import BaseModel
from pydantic.main import Extra


class Response(BaseModel, extra=Extra.forbid):
    status: bool
    message: str