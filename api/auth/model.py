from pydantic import BaseModel


class Token(BaseModel):
    jwt: str
    object: str
