from typing import Literal, Any
from pydantic import BaseModel

class ResponseError(BaseModel):

    status: Literal["fail"] = "fail"
    error: str

class ResponseSuccess(BaseModel):

    status: Literal["success"] = "success"
    data: Any
