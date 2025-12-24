from pydantic import BaseModel
from typing import Any

class Response(BaseModel):
    msg: str | None
    code: int
    data: Any | None


class OcrImageSerializer(BaseModel):
    image_url: str
    